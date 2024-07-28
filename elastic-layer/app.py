from flask import Flask, jsonify, request, Response
import os
from elasticsearch import Elasticsearch
import urllib3
import json
from search import *
import recommend
import update


http = urllib3.PoolManager()

# init flask app
app = Flask(__name__)

#create the elasticsearch client

username = 'elastic'
password = os.environ['ELASTIC_PASSWORD']

elastic_client = Elasticsearch(
    "http://elasticsearch-master:9200",
    basic_auth=(username, password)
)

#If no index user or listing created, create these
try:
    ## Create index for listing 
    elastic_client.indices.create(index ="listing")
    ## Create index for users 
    elastic_client.indices.create(index="user")

except:
    #index listing and user already exist.
    index_created = True


#from backend gateway file
DATA_URL = os.environ["DATA_URL"]
DATA_API_KEY = os.environ["DATA_API_KEY"]


#Responses
def make_invalid_request_response(message: str = ""):
    body = json.dumps({
        "message": message
    })
    return Response(body, status=400)


def make_not_found_response(message: str = ""):
    body = json.dumps({
            "message": message
        })
    return Response(body, status=404)



def make_internal_error_response():
    return Response(status=500)

def make_ok_response(body=None, headers: dict = None, auth: dict = None):
    if body != None:
        body = json.dumps(body)

    return Response(str(body), status=200)


def execute_data_request(http: urllib3.PoolManager, path, method, body):
    headers = {
        "X-Api-Key": DATA_API_KEY,
    }
    return http.request(method, f"http://{DATA_URL}{path}", body=body, headers=headers)


def getUserRecInfo(userId):
    return execute_data_request(http, path=f"/get_user_recommendation_info?userId={userId}", method="GET",  body=None)


def getSearchHistory(userid):
    result = execute_data_request(http, path=f"/get_search_history?userId={userid}", method="GET",  body=None)
    search_history = json.loads(result.data.decode('utf-8'))
    return search_history

# Helper functions for local testing
def loadListings():
    # listings =  execute_data_request(http, path='/get_all_listings', method="GET", body=None)
    
    # for now use static test data
    file = open('test_listings2.json')
    listings = json.load(file)
    file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)

def loadUsers():
    # users  = execute_data_request(http, path='/get_all_users', method="GET", body=None)

    # until backend hooked up
    file = open('test_users.json')
    users = json.load(file)
    file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)



# search path
# sample call: "localhost:4500/search?q=here+are+some+terms&type=user"
# NOTE: when calling this in command line with curl, may have to put url in " " to prevent zsh shell from thinking we're using special characters
# will need to add to search history eventually
@app.route('/search', methods=['GET'])
def route_search():

    query = request.args.get('q')
    if query == None:
        return make_invalid_request_response()

    user_results = searchVikeandSell(elastic_client, "user", query)
    listing_results =  searchVikeandSell(elastic_client, "listing", query)
    return make_ok_response(body={"listings": listing_results, "users": user_results})

# get recommendations call
# samplecall:  "localhost:4500/recommendations?userId=123"
@app.route('/recommendations',  methods=['GET'])
def route_recommendations():
    userId = request.args.get('userId')

    if userId == None:
        return make_invalid_request_response("userId required")

    response =  getUserRecInfo(userId)
    if response.status == 200:
        info = json.loads(response.data.decode('utf-8'))

        search_history = info["searches"]
        ignored = info["ignored"]
        results = recommend.recommend_algo(elastic_client, userId, search_history, ignored)
        return make_ok_response(body=results)

    elif response.status == 404:
        return make_not_found_response()
    else:
        return make_internal_error_response()


##  Basic test paths -------------------------------------------------
@app.route('/', methods=['GET'])
def welcome():
    return "Hello World"

@app.route('/test-es', methods=['GET'])
def test_es():
    info = elastic_client.info()
    return str(info)

#TODO: remove debug=True in Development
if __name__ == '__main__':
    app.run(debug=True)

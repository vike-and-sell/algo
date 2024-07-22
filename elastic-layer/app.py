from flask import Flask, jsonify, request
import os
from elasticsearch import Elasticsearch
import urllib3
import json
from search import *
import recommend


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
    ## Create index for listings 
    elastic_client.indices.create(index="user")

except:
    #index listing and user already exist.
    index_created = True


#from backend gateway file
DATA_URL = os.environ["DATA_URL"]
DATA_API_KEY = os.environ["DATA_API_KEY"]

#eventually add one for updating current listings

def execute_data_request(http: urllib3.PoolManager, path, method, body):
    headers = {
        "X-Api-Key": DATA_API_KEY,
    }
    result =  http.request(method, f"http://{DATA_URL}{path}", body=body, headers=headers)
    #response.data ##gives us something
    return json.loads(result.data.decode('utf-8'))


def getSearchHistory(userid):
    search_history = execute_data_request(http, path=f"/get_search_history?userId={userid}", method="GET",  body=None)
    
    #search_history = [{"search_date":"2024-01-01T00:00:00","search_text":"bike"}]
    return search_history

# search path
# sample call: "localhost:4500/search?q=here+are+some+terms&type=user"
# NOTE: when calling this in command line with curl, may have to put url in " " to prevent zsh shell from thinking we're using special characters
# will need to add to search history eventually
@app.route('/search', methods=['GET'])
def route_search():

    query = request.args.get('q')
    if query == None:
        return []

    user_results = searchVikeandSell(elastic_client, "user", query)
    listing_results =  searchVikeandSell(elastic_client, "listing", query)
    results = {
        'users' : user_results,
        'listings' : listing_results
    }
    # return results in JSON format
    return jsonify(results)

# get recommendations call
# samplecall:  "localhost:4500/recommendations?userId=123"
@app.route('/recommendations',  methods=['GET'])
def route_recommendations():
    userId = request.args.get('userId')

    if userId == None:
        return "Error: userId required"

    search_history = getSearchHistory(userId)
    results = recommend.recommend_algo(elastic_client, search_history)
    # return results in JSON format
    return results


# PATH: POST /recommendations/1/ignore?userId=1
# sample call: curl -X POST "http://localhost:4500/recommendations/5/ignore?userId=1"
@app.route('/recommendations/<listingId>/ignore', methods=['POST'])
def route_ignore_rec(listingId):

    userId = request.args.get('userId')
    #insert error message if none found
    if userId == None:
        return "Error: userId required"

    # add listing to "ignore" field for user in db
    # addIgnoredListing(userId, listingId)
    # update local copy
    result = recommend.ignore(elastic_client, userId, listingId)
    # make new set of recommendations, send to front end?

    return result


@app.route('/recommendations/ignore_charity', methods=['POST'])
def route_ignore_charity_rec():
    userId = request.args.get('userId')

    #TODO: 

    return "Not implemented"



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

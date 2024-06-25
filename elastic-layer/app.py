from flask import Flask, jsonify, request
import os
from elasticsearch import Elasticsearch
import urllib3
from search import *
import update
import recommend

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
    return http.request(method, f"http://{DATA_URL}{path}", json=body, headers=headers)


# Helper functions
def loadListings():
    listings =  execute_data_request('/get_all_listings', "GET", None)

    # for now use static test data
    # file = open('test_listings.json')
    # listings = json.load(file)
    # file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)


def loadUsers():
    users  = execute_data_request('/get_all_users', "GET", None)

    # until backend hooked up
    # file = open('test_users.json')
    # users = json.load(file)
    # file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)


def getSearchHistory(userid):
    search_history = execute_data_request(f"/get_search_history?userId={userid}", 'GET',  None)

    #search_history = ['bike']
    #update.loadElastic(elastic_client, 'search_history', 'user_id', search_history) # get specific name of id
    
    return search_history



# search path
#sample call: "localhost:4500/search?q=here+are+some+terms&type=user"
# NOTE: when calling this in command line with curl, may have to put url in " " to prevent zsh shell from thinking we're using special characters
@app.route('/search', methods=['GET'])
def test_search():
    #TODO:
    # add lat, long if we are responsible for location
    # get listings data from db if needed (?) interact with data layer.
    query = request.args.get('q')
    search_type = request.args.get('type')

    # hard code to assume listing if not user
    if search_type != 'user':
        search_type = 'listing'
    
    if search_type == "user":
        loadUsers()
    else:
        loadListings()

    results =  searchVikeandSell(elastic_client, search_type, query)
    
    # return results in JSON format option: jsonify(results)
    return results

# get recommendations call
# samplecall:  "localhost:4500/recommendations?userId=123"
@app.route('/recommendations',  methods=['GET'])
def test_get_rec():

    userId = request.args.get('userId')
    loadListings()
    search_history = getSearchHistory(userId)
    results = recommend.recommend_algo(elastic_client, search_history)
    # return results in JSON format
    return results


# TODO: SPRINT3:  update preferences call (block for now)
# PATH: POST /recommendations/{listingId}/ignore



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
from flask import Flask, jsonify, request

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from elasticsearch import Elasticsearch
import requests
##note requests does not support asynch http requests directly

from search import *
import update
import recommend


# init flask app
app = Flask(__name__)
#set up conn string for db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'],
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
)

# connect the app to the database
db = SQLAlchemy(app)

#create the elasticsearch client

username = 'elastic'
password = os.environ['ELASTIC_PASSWORD']

elastic_client = Elasticsearch(
    "http://elasticsearch:9200",
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


#Set urls to access backend endpoints 
url_get_history = os.environ['DATA_LAYER_URL'] + '/get_search_history/'
url_get_listings = os.environ['DATA_LAYER_URL'] + '/get_all_listings'
url_get_users = os.environ['DATA_LAYER_URL'] + '/get_all_users'
#eventually add one for updating current listings


# Helper functions
def loadListings():
    #listings =  requests.get(url_get_listings)

    # for now use static test data
    file = open('test_listings.json')
    listings = json.load(file)
    file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)


def loadUsers():
    #users  = requests.get(url_get_users)

    # until backend hooked up
    file = open('test_users.json')
    users = json.load(file)
    file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)


#Do not call this yet
def loadRecs(userid):

    search_history = requests.get(url_get_history + str(userid))
    update.loadElastic(elastic_client, 'search_history', 'id', search_history) # get specific name of id



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
@app.route('/rec/<userId>',  methods=['GET'])
def test_get_rec(userId):

    # TODO: ask DB for information associated with userid
    #loadRecs(userId)
    results = recommend.recommend(userId)
    # return results in JSON format
    return jsonify(results)


# TODO: SPRINT3:  update preferences call (block for now)
# PATH: POST /recommendations/{listingId}/ignore



##  Basic test paths -------------------------------------------------
@app.route('/', methods=['GET'])
def welcome():
    return "Hello World"

@app.route('/get_user', methods=['GET'])
def test_sql():
    result = db.session.execute(text("SELECT * FROM Users WHERE username = 'john_doe'"))
    rows = result.fetchall()
    return str(rows)

@app.route('/get_all_users', methods=['GET'])
def test_get_all():
    result = db.session.execute(text("SELECT * FROM Users"))
    rows = result.fetchall()
    return str(rows)


@app.route('/get_listings', methods=['GET'])
def test_getlisting():
    result = db.session.execute(text("SELECT * FROM Listings WHERE seller_id = 1"))
    rows = result.fetchall()
    return str(rows)

@app.route('/test-es', methods=['GET'])
def test_es():
    info = elastic_client.info()
    return str(info)

@app.route('/check_url', methods=['GET'])
def test_url():
    urls = [url_get_users, url_get_history, url_get_listings]
    return urls

#TODO: remove debug=True in Development
if __name__ == '__main__':
    app.run(debug=True)
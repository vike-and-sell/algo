from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from elasticsearch import Elasticsearch

from search import *
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


#load elastic client from database (untested)
def loadElastic():
    listings_index = 'listings'
    if not elastic_client.indices.exists(index=listings_index):
        elastic_client.indices.create(index=listings_index)

    #get listings from db (TODO)
    listings = db.session.execute(text("SELECT * FROM Listings"))
    cur_id = 0

    #load into listings index
    for entry in listings:
        cur_id  = cur_id + 1
        elastic_client.index(index=listings_index, id=cur_id, body=entry) #CHECK unless id = listing id from DB


    ## IF works, repeat for Users
    #get users from db 
    #users = db.session.execute(text("SELECT * FROM Users")


##  Basic test paths 
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

    # Validate and process the query parameters
    if search_type not in ['user', 'listing']:
        return 'Invalid search type. Allowed types are "user" and "listing".', 400
    
    results =  searchVikeandSell(elastic_client, search_type, query)
    # return results in JSON format
    return results
    #return jsonify(results)

# get recommendations call
@app.route('/recommendations/<userId>',  methods=['GET'])
def test_get_rec(userId):

    # TODO: ask DB for information associated with userid
    results = recommend.recommend_algo(elastic_client, userId)
    # return results in JSON format
    return results


# TODO: SPRINT3:  update preferences call (block for now)
# PATH: POST /recommendations/{listingId}/ignore


#TODO: remove debug=True in Development
if __name__ == '__main__':
    app.run(debug=True)
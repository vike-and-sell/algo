from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from elasticsearch import Elasticsearch

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


@app.route('/', methods=['GET'])
def welcome():
    return "Hello World"

@app.route('/get_user', methods=['GET'])
def test_sql():
    result = db.session.execute(text("SELECT * FROM Users WHERE username = 'john_doe'"))
    rows = result.fetchall()
    return str(rows)

@app.route('/test-es', methods=['GET'])
def test_es():
    info = elastic_client.info()
    return str(info)

# search call
@app.route('/search/<search_terms>', methods=['GET'])
def test_search(search_terms):
    # get terms from /search call -> is cleanest way to do this? what do we support?
    # terms = 
    # lat, long  = 
    # get listings data from db if needed (?)

    # results = search.getResults(terms, type, lat, long) ((type == user or listing))
    # 
    # return results in JSON
    return str(search_terms)


# get recommendations call
@app.route('/recommendations/<userId>',  methods=['GET'])
def test_get_rec(userid):
    # ask DB for information associated with userid
    ## lat, long??
    # results = recommend(userid, userinfo)
    # return results in JSON format

    return "recommendations: N/A"


# TODO: SPRINT3:  update preferences call (block for now)
# PATH: POST /recommendations/{listingId}/ignore


#TODO: remove debug=True in Development
if __name__ == '__main__':
    app.run(debug=True)
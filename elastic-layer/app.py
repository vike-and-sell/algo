from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from elasticsearch import ElasticSearch

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
password = os.getenv('ELASTIC_PASSWORD')

elastic_client = ElasticSearch(
    "http://localhost:9200",
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

if __name__ == '__main__':
    app.run(debug=True)
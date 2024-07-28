# This file will contain the unit tests that will test the search.py functionality
import pytest
import json
import os
import sys
import inspect
from elasticsearch import Elasticsearch

# This is needed so that we can import files from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import update
import search

''' Helper functions'''
# just define a global variable
username = 'elastic'
password = 'ElasticUser123'

elastic_client = Elasticsearch(
    "http://elasticsearch-master:9200",
    basic_auth=(username, password)
)
def loadListings():
    # listings =  execute_data_request(http, path='/get_all_listings', method="GET", body=None)
    
    # for now use static test data
    file = open(os.path.dirname(__file__) + '\\..\\test_listings2.json')
    listings = json.load(file)
    file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)

def loadUsers():
    file = open('..\\test_users.json')
    users = json.load(file)
    file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)

'''Test Functions'''
def test_listingInDatabaseSearch():
    loadListings()
    loadUsers()
    # using testing data loaded into the elastic database,
    # Preform a search for a specific item ie. "Bike"
    search_results = search.searchVikeandSell(elastic_client, "Listing", "Bike")
    # Remove the test data to ensure test is self contained
    elastic_client.delete()

    # and Assert that the listing returns the listing that is ensured to be in the database
    test_passing = 1
    expected_results = [] # TODO Fill this in with the result objects we are expecting
    for result in search_results:
        if result in expected_results:
            #we know the test should keep passing so do nothing
            continue
        else:
            test_passing = 0
    
    if test_passing is 0:
        assert False
    else:
        assert True

def test_listingNotInDatabaseSearch():
    loadListings()
    loadUsers()
    # knowing what testing data is loaded into the elastic database
    # Preform a search for a specific item ie. "Plane"
    search_results = search.searchVikeandSell(elastic_client, "Listing", "Plane")
    # Remove the test data to ensure test is self contained
    elastic_client.delete()

    expected_results = [] 
    if search_results is expected_results:
        assert True
    else:
        assert False

def test_userInDatabaseSearch():
    loadListings()
    loadUsers()
    # Given a user name contained in the testing data
    # Preform a search for that user
    search_results = search.searchVikeandSell(elastic_client, "User", "alice_wonder")
    # Remove the test data to ensure test is self contained
    elastic_client.delete()
    # Assert that the userId returned matches that of the corresponding user name in the testing data
    expected_result = {
      "user_id": 1,
      "username": "alice_wonder",
      "email": "alice@uvic.ca",
      "password": "Wonder123!",
      "location": { "latitude": 48.4284, "longitude": -123.3656 },
      "address": "1000 Wonderland Avenue, Victoria, BC",
      "joining_date": "2024-01-15",
      "items_sold": [101, 102],
      "items_purchased": [201, 202],
      "charity": True
    }

    if search_results is expected_result:
        assert True
    else:
        assert False

def test_userNotInDatabaseSearch():
    
    loadListings()
    loadUsers()
    # Given a user name not contained in the testing data
    # preform a search for that user
    search_results = search.searchVikeandSell(elastic_client, "User", "alice_wonder")
    # Remove the test data to ensure test is self contained
    elastic_client.delete()
    # Assert that no user is returned
    expected_result = []

    if search_results is expected_result:
        assert True
    else:
        assert False
    return False

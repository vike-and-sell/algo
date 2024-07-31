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
    "http://localhost:9200",
    basic_auth=(username, password)
)
def loadListings():
    # listings =  execute_data_request(http, path='/get_all_listings', method="GET", body=None)
    
    # for now use static test data
    file = open(os.path.dirname(__file__) + '//..//test_listings2.json')
    listings = json.load(file)
    file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)

def loadUsers():
    file = open(parentdir+'//test_users.json')
    users = json.load(file)
    file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)

'''Test Functions'''
def test_listingInDatabaseSearch():
    loadListings()
    loadUsers()
    # using testing data loaded into the elastic database,
    # Preform a search for a specific item ie. "Bike"
    search_results = search.searchVikeandSell(elastic_client, "listing", "Bike")

    # and Assert that the listing returns the listing that is ensured to be in the database
    test_passing = 1
    expected_results = [{'listing_id': 7, 'seller_id': 7, 'title': 'Mountain Bike', 'price': 200.0, 'location': {'latitude': 48.429, 'longitude': -123.365}, 'address': '123 Bike Trail, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-07-15T17:00:00', 'last_updated_at': '2024-07-15T17:00:00', 'charity': False}, 
                        {'listing_id': 11, 'seller_id': 2, 'title': 'Red Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '456 Cycle Street, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}, 
                        {'listing_id': 10, 'seller_id': 1, 'title': 'Blue Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '123 Bike Lane, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}, 
                        {'listing_id': 36, 'seller_id': 6, 'title': 'Electric Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '987 Shine Avenue, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}, 
                        {'listing_id': 37, 'seller_id': 6, 'title': 'Road Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '987 Shine Avenue, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}, 
                        {'listing_id': 12, 'seller_id': 3, 'title': 'Yellow Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '789 Pedal Avenue, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}, 
                        {'listing_id': 13, 'seller_id': 4, 'title': 'Green Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '321 Gear Road, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}, 
                        {'listing_id': 38, 'seller_id': 6, 'title': 'Gravel Bike', 'price': 20.0, 'location': {'latitude': 48.46, 'longitude': -123.31}, 'address': '987 Shine Avenue, Victoria, BC', 'status': 'AVAILABLE', 'listed_at': '2024-01-01T08:00:00', 'last_updated_at': '2024-01-01T08:00:00', 'charity': True}] 
    for result in search_results:
        if result in expected_results:
            #we know the test should keep passing so do nothing
            continue
        else:
            test_passing = 0
    
    if test_passing == 0:
        assert False
    else:
        assert True

def test_listingNotInDatabaseSearch():
    loadListings()
    loadUsers()
    # knowing what testing data is loaded into the elastic database
    # Preform a search for a specific item ie. "Plane"
    search_results = search.searchVikeandSell(elastic_client, "listing", "Plane")

    expected_results = [] 
    if search_results == expected_results:
        assert True
    else:
        assert False

def test_userInDatabaseSearch():
    loadListings()
    loadUsers()
    # Given a user name contained in the testing data
    # Preform a search for that user
    search_results = search.searchVikeandSell(elastic_client, "user", "alice_wonder")
    
    # Assert that the userId returned matches that of the corresponding user name in the testing data
    expected_result = [{'username': 'alice_wonder', 'user_id': 1}]

    if search_results is expected_result:
        assert True
    else:
        assert False

def test_userNotInDatabaseSearch():
    
    loadListings()
    loadUsers()
    # Given a user name not contained in the testing data
    # preform a search for that user
    search_results = search.searchVikeandSell(elastic_client, "user", "angus_is_the_coolest_ever")
    # Assert that no user is returned
    expected_result = []

    if search_results == expected_result:
        assert True
    else:
        assert False
    return False

# This file will contain the unit tests for the recomment.py file
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

'''# Helper functions'''
# just define a global variable
username = 'elastic'
password = 'ElasticUser123'

elastic_client = Elasticsearch(
    "http://elasticsearch-master:9200",
    basic_auth=(username, password)
)
def loadListings():
    print("LoadListings", Flush=True)
    # listings =  execute_data_request(http, path='/get_all_listings', method="GET", body=None)
    
    # for now use static test data
    file = open('..\\test_listings2.json')
    listings = json.load(file)
    file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)

def loadUsers():
    # users  = execute_data_request(http, path='/get_all_users', method="GET", body=None)

    # until backend hooked up
    file = open('..\\test_users.json')
    users = json.load(file)
    file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)

'''Test Functions'''
def test_noSearchHistoryRecommendation():
    # Load the test data
    
    # Given a user

    # Get the recommendations for that user based on their search history
    # Since the user has no search history ensure that the results are the default values we want for a cold start

    # Remove the test data to ensure test is self contained

    # If they are the default results
        # Assert true
    # else
        # Assert False

    
    assert False

def test_searchHistoryRecommendation():
    # Given a userId
    # Get the recommendations for that user based on their search history
        # Ensure that a testing user is used with a defined search history
    # Since the user has a defined search history, ensure that the results are what has been defined in the code
    # If the results are correct
        # Assert True
    # else
        # Assert False
    return False

def test_noDuplicateItemsInRecommendation():
    # Given a userId (with no search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs returned are the same

    # Given a userId (with a search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs return are the same
    return False # No return should be needed depending on the testing framework used

def test_charityItemsFirst():
    # For a userId (with no search history)
    # Get the recommendation for that usesr
    # Assert that no charity listings are returned after the first non-charity listing

    # Repeete above for user with a search history
    return False
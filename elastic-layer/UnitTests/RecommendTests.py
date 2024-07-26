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
import recommend

'''# Helper functions'''
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
def test_noSearchHistoryRecommendation():
    # Load the test data
    loadListings()
    loadUsers()
    
    # Given a user. user_id = 1
    # Get the recommendations for that user based on their search history
    # Since the user has no search history ensure that the results are the default values we want for a cold start
    recommended_results = recommend.recommend_algo(elastic_client, "")
    
    # Remove the test data to ensure test is self contained
    elastic_client.delete()

    # Check to see if all the returned resluts are what we expect to be getting
    testPassed = 1
    for result in recommended_results:
        if result not in (): # TODO fill this in with the expected results
            testPassed = 0

    if testPassed is not 0:
        assert True
    else:
        assert False

def test_searchHistoryRecommendation():
    # Load the test data
    loadListings()
    loadUsers()

    # Given a user. user_id = 1
    # Get the recommendations for that user based on their search history
        # Ensure that a testing user is used with a defined search history
    # Since the user has a defined search history, ensure that the results are what has been defined in the code
    search_history = [] #TODO fill in the search history
    recommended_results = recommend.recommend_algo(elastic_client, search_history)

    testPassed = 1
    for result in recommended_results:
        if result not in (): # TODO fill this in with the expected results
            testPassed = 0

    if testPassed is not 0:
        assert True
    else:
        assert False

def test_noDuplicateItemsInRecommendation():
    # Given a userId (with no search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs returned are the same
    recommended_results = recommend.recommend_algo(elastic_client, "")
    while recommended_results is not []:
        result1 = recommended_results.pop()
        for result2 in recommended_results:
            if result1 is result2:
                assert False

    # Given a userId (with a search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs return are the same
    search_history = [] #TODO fill in the search history
    recommended_results = recommend.recommend_algo(elastic_client, search_history)
    while recommended_results is not []:
        result1 = recommended_results.pop()
        for result2 in recommended_results:
            if result1 is result2:
                assert False

    assert True

def test_charityItemsFirst():
    # For a userId (with no search history)
    # Get the recommendation for that usesr
    # Assert that no charity listings are returned after the first non-charity listing
    recommended_results = recommend.recommend_algo(elastic_client, "")
    while recommended_results is not []:
        result1 = recommended_results.pop()
        for result2 in recommended_results:
            if result1.for_charity is False and result2.for_charity is True:
                assert False

    # Repeete above for user with a search history
    
    search_history = [] #TODO fill in the search history
    recommended_results = recommend.recommend_algo(elastic_client, search_history)
    while recommended_results is not []:
        result1 = recommended_results.pop()
        for result2 in recommended_results:
            if result1.for_charity is False and result2.for_charity is True:
                assert False
    return False
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
    file = open(os.path.dirname(__file__) + '\\..\\test_listings2.json')
    listings = json.load(file)
    file.close

    update.loadElastic(elastic_client, 'listing', 'listing_id', listings)

def loadUsers():
    file = open(parentdir+'//test_users.json')
    users = json.load(file)
    file.close

    update.loadElastic(elastic_client,'user', 'user_id', users)

'''Test Functions'''
def test_noSearchHistoryRecommendation():
    # Load the test data
    loadListings()
    loadUsers()
    f = open(currentdir+"//noSearchHistoryRecommendationJSON.txt", "r")

    # Given a user. user_id = 1
    # Get the recommendations for that user based on their search history
    # Since the user has no search history ensure that the results are the default values we want for a cold start
    recommended_results = recommend.recommend_algo(elastic_client, "1", search_history="", do_not_rec=[])
    if str(recommended_results) != f.read(): 
        assert False
    

    assert True

def test_searchHistoryRecommendation():
    # Load the test data
    loadListings()
    loadUsers()
    f = open(currentdir+"//searchHistoryRecommendationJSON.txt", "r")

    # Given a user. user_id = 1
    # Get the recommendations for that user based on their search history
        # Ensure that a testing user is used with a defined search history
    # Since the user has a defined search history, ensure that the results are what has been defined in the code
    search_history = ["bike", "table", "tool"] 
    recommended_results = recommend.recommend_algo(elastic_client, "1", search_history, [])
    if str(recommended_results) != f.read(): 
        assert False

    assert True

def test_noDuplicateItemsInRecommendation():
    # Given a userId (with no search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs returned are the same
    recommended_results = recommend.recommend_algo(elastic_client, "1", "", [])
    while recommended_results:
        result1 = recommended_results.pop()
        for result2 in recommended_results:
            if result1 is result2:
                assert False

    # Given a userId (with a search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs return are the same
    search_history = ["bike", "table", "tool"]
    recommended_results = recommend.recommend_algo(elastic_client, "1", search_history, [])
    while recommended_results:
        result1 = recommended_results.pop()
        for result2 in recommended_results:
            if result1 is result2:
                assert False

    assert True

def test_charityEnabledAndDisabled():
    # Given a user that wants to see charity items (USER 1)
    # Get recomendation results and ensure that there is at least one charity
    
    recommended_results = recommend.recommend_algo(elastic_client, "1", "", [])
    charity_item = 0 # start assuming that there are no charity items
    for result in recommended_results:
        if result.get('charity'):
            charity_item = 1
        
    if charity_item == 0: # no charity item was found
        assert False

    # Given a user that does not want to see charity items (USER 2)
    # Get recomendation results and ensure that there are no charity items
    recommended_results = recommend.recommend_algo(elastic_client, "2", "", [])
    for result in recommended_results:
        if result.get('charity'):
            charity_item = 1
        
    if charity_item == 1: # a charity item was found
        assert False
    
    # If all checks passed
    assert True

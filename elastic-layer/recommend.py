from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json
from search import *
from update import *

## Recommend function called by app.py on reccomend request.
# returns a list of listings in JSON format
def recommend_algo(elastic_client, search_history):
    print("recommending from Vike and sell..... ")
    #test_data(elastic_client)
    # #search history now has format of: {"search_date":"2024-01-01T00:00:00","search_text":"Hot Wheels"},{"search_date":"2024-01-02T00:00:00","search_text":"iPod touch 5th Gen"}]

    ## Where the recommender magic will happen
    ## Preload with invalid data for the backend to compare against
    return_data = [] 

    # before looping through all search history results truncate it to the top 10 results
    for result in search_history:
        response = searchVikeandSell(elastic_client, "listing", result.get("search_text"))
        
        #bandaid fix by haley so it doesn't break when recommendations are made
        return response

        count = 0
        for hit in response:
            if count <= 5:
                # Don't add duplicate item to the list
                return_data.append(hit)
                count = count + 1
            else:
                continue

    # This makes sure that if data is returned then it is a propper reccomendation
    # if False is returned then an error occured
    if return_data is not []:
        return return_data
    else:
        return ("No recommendations can be made at this time")
    
def get_search_history(userId):
    return ["bike"] # list of one item
    
# def test_data(elastic_client):
#     #Create test listing
#     test_listing = { "SellerID": "User1", 
#                     "ListingID": "1", 
#                     "Title": "Blue Bike",  
#                     "Description": "Very good bike", 
#                     "Price": "20", 
#                     "Location": "48.46, -123.31",  
#                     "Status": "Available" }

#     ID = test_listing.get('ListingID')
#     #Add test listing to index listing
#     add_doc(elastic_client, "listing", ID, test_listing)

#     #Create test listing
#     test_listing = { "SellerID": "User2", 
#                     "ListingID": "2", 
#                     "Title": "Red Bike",  
#                     "Description": "Very good bike", 
#                     "Price": "20", 
#                     "Location": "48.46, -123.31",  
#                     "Status": "Available" }

#     ID = test_listing.get('ListingID')
#     #Add test listing to index listing
#     add_doc(elastic_client, "listing", ID, test_listing)

#     #Create test listing
#     test_listing = { "SellerID": "User3", 
#                     "ListingID": "3", 
#                     "Title": "Yellow Bike",  
#                     "Description": "Very good bike", 
#                     "Price": "20", 
#                     "Location": "48.46, -123.31",  
#                     "Status": "Available" }

#     ID = test_listing.get('ListingID')
#     #Add test listing to index listing
#     add_doc(elastic_client, "listing", ID, test_listing)

#     #Create test listing
#     test_listing = { "SellerID": "User4", 
#                     "ListingID": "4", 
#                     "Title": "Green Bike",  
#                     "Description": "Very good bike", 
#                     "Price": "20", 
#                     "Location": "48.46, -123.31",  
#                     "Status": "Available" }

#     ID = test_listing.get('ListingID')
#     #Add test listing to index listing
#     add_doc(elastic_client, "listing", ID, test_listing)

    # test_user = {   "UserID": "User1",
    #                 "Location": "48.46, -123.31",
    #                 "Age": "20",
    #                 "SearchHistory": "Bike"
    # }
    # ID = test_user.get("UserID")
    # add_doc(elastic_client, "user", ID, test_user)

    # test_user = {   "UserID": "User2",
    #                 "Location": "48.46, -123.31",
    #                 "Age": "20",
    #                 "SearchHistory": "Bike"
    # }
    # ID = test_user.get("UserID")
    # add_doc(elastic_client, "user", ID, test_user)

    # test_user = {   "UserID": "User3",
    #                 "Location": "48.46, -123.31",
    #                 "Age": "20",
    #                 "SearchHistory": "Bike"
    # }
    # ID = test_user.get("UserID")
    # add_doc(elastic_client, "user", ID, test_user)

    # test_user = {   "UserID": "User4",
    #                 "Location": "48.46, -123.31",
    #                 "Age": "20",
    #                 "SearchHistory": "Bike"
    # }
    # ID = test_user.get("UserID")
    # add_doc(elastic_client, "user", ID, test_user)

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json

from update import *

## Search function called by app.py on search request.
# returns a list of listings in JSON format
def searchVikeandSell(elastic_client, search_type, search_terms):
    print("searching Vike and sell..... ")

    results = []

    context = Search(using = elastic_client, index = search_type) 
    s = context.query('query_string', query = search_terms)
    response = s.execute()


    if search_type == 'user':
        if response.success():
            for hit in response:
                ##IN THE REAL SEARCH WILL USE userid?
                results.append(hit.username)
    else:
        if response.success():
            for hit in response:
                ##IN THE REAL SEARCH WILL USE LISTINGID!
                results.append(hit.title)
                print(hit.title)

    return results


# def test_data_add(elastic_client):


#     file = open('test_listings.json')
#     test_listings = json.load(file)
#     file.close

#     loadElastic(elastic_client, 'listing', 'listing_id', test_listings)


    # test_listing = { "SellerID": "User1", 
    #                 "ListingID": "1", 
    #                 "Title": "Blue Bike",  
    #                 "Description": "Very good bike", 
    #                 "Price": "20", 
    #                 "Location": "48.46, -123.31",  
    #                 "Status": "Available" }

    # ID = test_listing.get('ListingID')
    # #Add test listing to index listing
    # add_doc(elastic_client, "listing", ID, test_listing)

    # #Create test listing
    # test_listing = { "SellerID": "User2", 
    #                 "ListingID": "2", 
    #                 "Title": "Red Bike",  
    #                 "Description": "Very good bike", 
    #                 "Price": "20", 
    #                 "Location": "48.46, -123.31",  
    #                 "Status": "Available" }

    # ID = test_listing.get('ListingID')
    # #Add test listing to index listing
    # add_doc(elastic_client, "listing", ID, test_listing)

    # #Create test listing
    # test_listing = { "SellerID": "User3", 
    #                 "ListingID": "3", 
    #                 "Title": "Yellow Bike",  
    #                 "Description": "Very good bike", 
    #                 "Price": "20", 
    #                 "Location": "48.46, -123.31",  
    #                 "Status": "Available" }

    # ID = test_listing.get('ListingID')
    # #Add test listing to index listing
    # add_doc(elastic_client, "listing", ID, test_listing)
    # #Create test listing
    # test_listing = { "SellerID": "User4", 
    #                 "ListingID": "4", 
    #                 "Title": "Green Bike",  
    #                 "Description": "Very good bike", 
    #                 "Price": "20", 
    #                 "Location": "48.46, -123.31",  
    #                 "Status": "Available" }

    # ID = test_listing.get('ListingID')
    # #Add test listing to index listing
    # add_doc(elastic_client, "listing", ID, test_listing)

    # #Create test listing
    # test_listing = { "SellerID": "User5", 
    #                 "ListingID": "5", 
    #                 "Title": "Green Lamp",  
    #                 "Description": "Very good lamp", 
    #                 "Price": "20", 
    #                 "Location": "48.46, -123.31",  
    #                 "Status": "Available" }

    # ID = test_listing.get('ListingID')
    # #Add test listing to index listing
    # add_doc(elastic_client, "listing", ID, test_listing)

    # #Create test listing
    # test_listing = { "SellerID": "User6", 
    #                 "ListingID": "6", 
    #                 "Title": "Yellow Lamp",  
    #                 "Description": "Very good lamp", 
    #                 "Price": "20", 
    #                 "Location": "48.46, -123.31",  
    #                 "Status": "Available" }

    # ID = test_listing.get('ListingID')
    # #Add test listing to index listing
    # add_doc(elastic_client, "listing", ID, test_listing)

#searchVikeandSell(elastic_client, "listing", "bike")
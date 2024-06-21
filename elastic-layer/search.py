from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search

from update import *

import os
import json

## Search function called by app.py on search request.
# returns a list of listings in JSON format
def searchVikeandSell(search_type, search_terms):
    print("searching Vike and sell..... ")

    # where the search magic will happen
    #Search magic
    context = Search(using = elastic_client, index = search_type) 
    s = context.query('query_string', query = search_terms)
    response = s.execute()

    if response.success():
        for hit in response:
            print(hit.Title)

    return response

#Create test listing
test_listing = { "SellerID": "User1", 
                "ListingID": "1", 
                "Title": "Blue Bike",  
                "Description": "Very good bike", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')
#Add test listing to index listing
add_doc("listing", ID, test_listing)

#Create test listing
test_listing = { "SellerID": "User2", 
                "ListingID": "2", 
                "Title": "Red Bike",  
                "Description": "Very good bike", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')
#Add test listing to index listing
add_doc("listing", ID, test_listing)

#Create test listing
test_listing = { "SellerID": "User3", 
                "ListingID": "3", 
                "Title": "Yellow Bike",  
                "Description": "Very good bike", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')
#Add test listing to index listing
add_doc("listing", ID, test_listing)

#Create test listing
test_listing = { "SellerID": "User4", 
                "ListingID": "4", 
                "Title": "Green Bike",  
                "Description": "Very good bike", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')
#Add test listing to index listing
add_doc("listing", ID, test_listing)

#Create test listing
test_listing = { "SellerID": "User5", 
                "ListingID": "5", 
                "Title": "Green Lamp",  
                "Description": "Very good lamp", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')
#Add test listing to index listing
add_doc("listing", ID, test_listing)

#Create test listing
test_listing = { "SellerID": "User6", 
                "ListingID": "6", 
                "Title": "Yellow Lamp",  
                "Description": "Very good lamp", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')
#Add test listing to index listing
add_doc("listing", ID, test_listing)

#Search
searchVikeandSell("listing", "lamp")

#Delete doc delete_doc(search_type, doc_ID, data)
delete_doc("listing", ID, test_listing)

#Search again after deleting
searchVikeandSell("listing", "lamp")


#Update a doc
#Test test listing
test_listing = { "SellerID": "User5", 
                "ListingID": "5", 
                "Title": "Green Lamp with flowers",  
                "Description": "Very very good lamp", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" }

ID = test_listing.get('ListingID')

#Update doc delete_doc(search_type, doc_ID, data)
update_doc("listing", ID, test_listing)

#Search again after deleting
searchVikeandSell("listing", "flowers")
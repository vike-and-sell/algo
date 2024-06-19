from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json

## Search function called by app.py on search request.
# returns a list of listings in JSON format
def searchVikeandSell(search_type, search_terms):
    print("searching Vike and sell..... ")

    # where the search magic will happen

    dummy_data = [{ "SellerID": "User2", 
                "ListingID": "44", 
                "Title": "Green Lamp",  
                "Description": "Very good lamp", 
                "Price": "20", 
                "Location": "48.46, -123.31",  
                "Status": "Available" },
                { "SellerID": "User1", 
                "ListingID": "123", 
                "Title": "Yellow Lamp",  
                "Description": "Very good lamp", 
                "Price": "20", 
                "Location": "48.46, -123.31", 
                "Status": "Available" }]

    return dummy_data

#Temp fix for authentication issues, will need to fix this later
username = "elastic"
password = "ElasticUser123"

##Establish elasticsearch connection
elastic_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(username, password)
)

## Ping Elasticsearch to ensure it is up 
#print(elastic_client.ping())

def LarissaCode():
    ##Delete old indices, this will need to be removed in final version
    # elastic_client.indices.delete(index = "listings")
    #elastic_client.indices.delete(index = "users")

    ## Create index for listings 
    elastic_client.indices.create(index = "listings")

    ## Create index for listings 
    elastic_client.indices.create(index="users")


    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "123", 
                    "Title": "Blue Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    #Add test listing to index listing
    doc = elastic_client.index(index = 'listings', id = 1, body = test_listing)

    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "123", 
                    "Title": "Red Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    #Add test listing to index listing
    doc = elastic_client.index(index = 'listings', id = 2, body = test_listing)

    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "123", 
                    "Title": "Yellow Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    #Add test listing to index listing
    doc = elastic_client.index(index = 'listings', id = 3, body = test_listing)

    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "123", 
                    "Title": "Green Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    #Add test listing to index listing
    doc = elastic_client.index(index = 'listings', id = 4, body = test_listing)

    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "123", 
                    "Title": "Green Lamp",  
                    "Description": "Very good lamp", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    #Add test listing to index listing
    doc = elastic_client.index(index = 'listings', id = 5, body = test_listing)

    elastic_client.indices.refresh(index = "listings")

    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "123", 
                    "Title": "Yellow Lamp",  
                    "Description": "Very good lamp", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    #Add test listing to index listing
    doc = elastic_client.index(index = 'listings', id = 6, body = test_listing)

    elastic_client.indices.refresh(index = "listings")


    #Search
    context = Search(using = elastic_client, index = 'listings', doc_type = 'doc') 

    s = context.query('query_string', query = 'lamp')
    response = s.execute()

    if response.success():
        for hit in response:
            print(hit.Title)


    #Add a listing document to the index
    #def add_listing_doc(listing):

    
    #Add a user document to the index
    #def add_user_doc(user):


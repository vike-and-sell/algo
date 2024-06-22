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

    dummy_data = [{"searchType" : search_type,
                "searchTerms" : str(search_terms)}]

    return dummy_data

#Temp fix for authentication issues, will need to fix this later
username = "elastic"
password = "ElasticUser123"

##Establish elasticsearch connection
elastic_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(username, password)
)


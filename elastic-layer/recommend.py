from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json

## Recommend function called by app.py on reccomend request.
# returns a list of listings in JSON format
def recommend(userId):
    print("recommending from Vike and sell..... ")

    ## Where the recommender magic will happen
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
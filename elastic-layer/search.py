from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import json

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

##Delete old indices
elastic_client.indices.delete(index = "listings")
##elastic_client.indices.delete(index = "users")

## Create index for listings 
elastic_client.indices.create(index = "listings")
test_listing = { "SellerID": "User1", "ListingID": "123", "Title": "Blue Bike",  "Description": "Very good bike", "Price": "20", "Location": "48.46, -123.31",  "Status": "Available" }

doc = elastic_client.index(index = 'listings', id = 1, body = test_listing)

print(doc["result"])

## Create index for listings 
#elastic_client.indices.create(index="users")



##Add single Entry



#Add a listing document to the index
#def add_listing_doc(listing):

   
#Add a user document to the index
#def add_user_doc(user):


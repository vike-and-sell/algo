from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search

import os
import json

## Will include all logic for updating the elasticsearch DB
## Need to add users and listings
## Need to delete users and listings
## Need to update users and listings

#Temp fix for authentication issues, will need to fix this later TO FIX
username = "elastic"
password = "ElasticUser123"

##Establish elasticsearch connection
elastic_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=(username, password)
)

##Only for testing TO REMOVE
elastic_client.indices.delete(index="listing")
elastic_client.indices.delete(index="user")

#If not index user or listing created, create these
try:
    ## Create index for listing 
    elastic_client.indices.create(index = "listing")
    ## Create index for listings 
    elastic_client.indices.create(index="user")

except:
    #index listing and user already exist.
    index_created = True


#Add doc to index listings or users
def add_doc(search_type, doc_ID, data):
    doc = elastic_client.index(index = search_type, id = doc_ID, body = data)
    elastic_client.indices.refresh(index = search_type)

   

#Update doc from index listings or users
def update_doc(search_type, doc_ID, data):
    doc = elastic_client.index(index = search_type, id = doc_ID, body = data)
    elastic_client.indices.refresh(index = search_type)



#Delete doc from index listings or users
def delete_doc(search_type, doc_ID, data):
    elastic_client.delete(index = search_type, id = doc_ID)
    elastic_client.indices.refresh(index = search_type)

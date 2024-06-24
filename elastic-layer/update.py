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
# try:
#     elastic_client.indices.delete(index="listing")
#     elastic_client.indices.delete(index="user")

# except:
#     index_create = True

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

#load elastic client with listings
# index_name = a string containing name of index
# id_title = a string of the expected name associated with the id of the object (listing_id, user_id, etc.) within the JSON file
# Json list = list of json objects to be added to elasticclient index as documents
def loadElastic(index_name, id_title, json_list):
    
    #for now, delete the indices if already exists. this is to ensure no lingering old docs for now.
    if elastic_client.indices.exists(index=index_name):
        elastic_client.indices.delete(index=index_name)

    elastic_client.indices.create(index=index_name)

    #load into listings index
    for entry in json_list:
        cur_id = entry.get(id_title)
        print(entry)
        add_doc(index_name, cur_id, entry)
        #elastic_client.index(index=index_name, id=cur_id, body=entry) #CHECK unless id = listing id from DB

    elastic_client.indices.refresh(index = index_name)


def getClient():
    return elastic_client

def test1():
    file = open('test_listings.json')
    test_listings = json.load(file)
    file.close

    name = 'test1'
    idtitle = 'ListingID'

    search_terms = "bike"

    print("trying to load...")
    loadElastic(name, idtitle, test_listings)
 
    print("searching...")
    elastic_client.indices.refresh(index = name)
    context = Search(using = elastic_client, index = name) 
    s = context.query('query_string', query = search_terms)
    response = s.execute()

    if response.success():
        for hit in response:
            print(hit.Title)
    else:
        print("search failed")

    print("exiting..")



test1()

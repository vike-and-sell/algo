from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search

import os
import json

## This file includes all the logic to add, update, or delete Users or Listings from the Database

#Add doc to index listings or users
def add_doc(elastic_client, search_type, doc_ID, data):
    print(search_type)
    print(data)
    try:
        elastic_client.index(index = search_type, id = doc_ID, body = data)
        elastic_client.indices.refresh(index = search_type)
    except:
        print("Could not add")

   
#Update doc from index listings or users
def update_doc(elastic_client, search_type, doc_ID, data):
    doc = elastic_client.index(index = search_type, id = doc_ID, body = data)
    elastic_client.indices.refresh(index = search_type)



#Delete doc from index listings or users
def delete_doc(elastic_client, search_type, doc_ID, data):
    elastic_client.delete(index = search_type, id = doc_ID)
    elastic_client.indices.refresh(index = search_type)

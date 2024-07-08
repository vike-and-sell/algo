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
                #Frontend needs list of seller_id
                results.append(hit.user_id)
    else:
        if response.success():
            for hit in response:
                ##Frontend needs list of user_id
                ID = hit.listing_id
                doc = elastic_client.get(index = "listing", id = ID)
                results.append(doc["_source"])

    #Returns the results in JSON format
    return results

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json

from update import *

SEARCH_SIZE = 200
## Search function called by app.py on search request.
# returns a list of listings in JSON format
def searchVikeandSell(elastic_client, search_type, search_terms):
    results = []

#SEARCH USERS
    if search_type == 'user':
    #User Search Query
        search_terms = '*' + search_terms + '*'
        query = { 
            "size" : SEARCH_SIZE,
            "query": {
                "wildcard": {
                    "username": {
                        "value": search_terms,
                        "case_insensitive": True
                    }
                }
            }
        }

        #Search for documents
        response = elastic_client.search(index=search_type, body=query)
        hits = response["hits"]["hits"]

        #Format the search results to return as a JSON
        for hit in hits:
            #Ensures no duplicates are added
            if hit not in results:
                user_hit = hit["_source"]
                name = user_hit.get('username')
                id = user_hit.get('user_id')
                body={"username": name, "user_id": id }
                results.append(body)

#SEARCH LISTINGS
    else:
    #Listing Search Query
        query = { 
            "size" : SEARCH_SIZE,
	        "query": {
                "bool": {
                    "must": [
                        {   
                        "match": {"title": search_terms}
                        }
                    ]
                } 
	        }
        }

        #Search for documents
        response = elastic_client.search(index=search_type, body=query)
        hits = response["hits"]["hits"]

        #Format the search results to return as a JSON
        for hit in hits:
            #Ensures no duplicates are added
            if hit not in results:
                results.append(hit["_source"])

    #Returns the results in JSON format
    return results

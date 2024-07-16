from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json

from update import *

## Search function called by app.py on search request.
# returns a list of listings in JSON format
def searchVikeandSell(elastic_client, search_type, search_terms):
    results = []

    search_terms = search_terms + "*"
    
    if search_type == 'user':
    #User Search Query
        query = { 
	        'query': {
                    "wildcard": 
                        {   
                        'username': search_terms
                        }
	        }
        }

        #Search for documents
        response = elastic_client.search(index=search_type, body=query)
        hits = response["hits"]["hits"]

        #Format the search results to return as a JSON
        for hit in hits:
            results.append(hit["_source"])

    else:
    #Listing Search Query
        #define the search query
        query = { 
	        "query": {
                "bool": {
                    "must": [
                        {   
                        "match": {"title": search_terms}
                        },
                        {
                        "match": {"status": "AVAILABLE"}
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
            results.append(hit["_source"])

    #Returns the results in JSON format
    return results

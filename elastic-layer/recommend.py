from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json
from search import *
from update import *


## Recommend function called by app.py on reccomend request.
# returns a list of listings in JSON format
def recommend_algo(elastic_client, search_history):
    #test_data(elastic_client)
   
    ## Preload with invalid data for the backend to compare against
    return_data = [] 

    # before looping through all search history results truncate it to the top 10 results
    for s in search_history:
        response = searchVikeandSell(elastic_client, "listing", s)
        
        count = 0
        for hit in response:
            if count < 3:
                # Don't add duplicate item to the list
                return_data.append(hit)
                count = count + 1
            

    # This makes sure that if data is returned then it is a propper reccomendation
    # if False is returned then an error occured

    if (len(return_data) > 25): #10 for now but should be more when we have more test listings
        return return_data

    else:
        #return ("No recommendations can be made at this time")
        num_recs = len(return_data)
        
        #No listing match the Users search history, so will use cold start data\
        cold_start_rec = ['bike', 'lamp', 'table', 'chair', 'clothes', 'Sale', 'Vintage'] #TBD on what will be listed here
        for s in cold_start_rec:
            response = searchVikeandSell(elastic_client, "listing", s)
        
            count = 0
            for hit in response:
                if count < 3:
                    # Don't add duplicate item to the list
                    return_data.append(hit)
                    count = count + 1

                
            if (len(return_data) > 25):
                return return_data

        return return_data
    
def get_search_history(userId):
    return ["bike"] # list of one item
    
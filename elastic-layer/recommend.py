from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json
from search import *
from update import *

NUM_HISTORY_RECS = 8
COLD_START_RECS = 5
TOTAL_REC_RETURN = 25

show_charity = 1
do_not_show = [7, 10] # This will be list of listing IDS???


## Recommend function called by app.py on reccomend request.
## Returns a list of listings in JSON format
def recommend_algo(elastic_client, search_history): # need to add "do_not_show"
   
    ## Preload with invalid data for the backend to compare against
    return_data = [] 
    do_not_show = [7, 10]

    #Recommendations made based on user search history
    for s in search_history:
        response = searchVikeandSell(elastic_client, "listing", s)
        
        #bandaid fix by haley so it doesn't break when recommendations are made
        return response

        count = 0
        for hit in response:
            if count < NUM_HISTORY_RECS:

                # Need to get listing_ID in order to compare
                listing_id = hit.get('listing_id')

                #Only add to results if listing is not in the do not recommend user list
                if listing_id not in do_not_show:
                    return_data.append(hit)
                
                count = count + 1

            if (len(return_data) > TOTAL_REC_RETURN): 
                return return_data   
                

    ## If there are not enough listings that match the users search history, will continue with cold data search history
        
    # Not enough listings match the Users search history, so will use cold start data
    cold_start_rec = ['bike', 'lamp', 'table', 'chair', 'clothes', 'sale', 'Vintage']

    for s in cold_start_rec:
        response = searchVikeandSell(elastic_client, "listing", s)
        
        count = 0
        for hit in response:
            if count < COLD_START_RECS:
                # Need to get listing_ID in order to compare
                listing_id = hit.get('listing_id')

                #Only add to results if listing is not in the do not recommend user list
                if listing_id not in do_not_show:
                    return_data.append(hit)
                
                count = count + 1


            if (len(return_data) > TOTAL_REC_RETURN):
                return return_data

    return return_data
    
#Do we need?
def get_search_history(userId):
    return ["bike"] # list of one item
    
def ignore(elastic_client, userId, listingId):

    # TODO: ignore the listing given in recommendations.

    # adjust recommendations given based on ignore? 
    return "not implemented"

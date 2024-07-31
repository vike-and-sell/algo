from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search
import os
import json
from search import *
from update import *

NUM_HISTORY_RECS = 10
TOTAL_REC_RETURN = 200
NUM_SIMILAR_RECS = 5


## Recommend function called by app.py on reccomend request.
## Returns a list of listings in JSON format
def recommend_algo(elastic_client, userId, search_history, do_not_rec):
   
    return_data = [] 
    
    #Check if user has Charity items enabled
    see_charity = get_charity_value(elastic_client, userId)

    #Find similar listing to the do_not_rec lists
    do_not_show = do_not_recommend_type(elastic_client, do_not_rec)

    #If user has no search history, cold start
    if len(search_history) == 0:
         return cold_start(elastic_client, userId, return_data, see_charity, do_not_show)
    
    #Make newest search history the most relevant
    search_history.reverse()

    #Recommender logic
    for s in search_history:
        response = rec_search(elastic_client, 'listing', s, see_charity)

        count = 0
        for hit in response:
            if count < NUM_HISTORY_RECS:

                #Check for duplicates
                if hit not in return_data:

                    # Need to get listing_ID in order to compare
                    listing_id = hit.get('listing_id')

                    #Only add to results if listing is not in the do not recommend user list
                    if listing_id not in do_not_show:
                        return_data.append(hit)
                
                    count = count + 1

                if (len(return_data) > TOTAL_REC_RETURN): 
                    return return_data   
    
    #If we do not have enough recomendations, call cold_start
    if (len(return_data) < TOTAL_REC_RETURN): 
        results = cold_start(elastic_client, userId, return_data, see_charity, do_not_show)
        return results 

    return return_data
    



    
def rec_search(elastic_client, search_type, search_terms, see_charity):
    results = []

    #Listing Search Query
    query = { 
        "size" : NUM_SIMILAR_RECS,
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
        #Check if listing is marked for charity
        listing_hit = hit["_source"]
        marked_for_charity = listing_hit.get('charity') 

        if (marked_for_charity == True):
            if(see_charity == True):
                results.append(hit["_source"])

        else:
            #item is not marked for charity can can be added
            results.append(hit["_source"])

    #Search for documents
    return results




def cold_start(elastic_client, userId, return_data, see_charity, do_not_show):

    query = { 
        "size" : TOTAL_REC_RETURN,
        "query": {
            "match_all": {}
        }
    }

    #Search for documents
    response = elastic_client.search(index="listing", body=query)
    hits = response["hits"]["hits"]

    for hit in hits:
        #Ensures no duplicates are added
        listing_hit = hit["_source"]
        if listing_hit not in return_data:
            #Check if listing is marked for charity
            marked_for_charity = listing_hit.get('charity') 

            #Get listingId for do not rec compare
            listing_id = listing_hit.get('listing_id')

            #Only add to results if listing is not in the do not recommend user list
            if listing_id not in do_not_show:
                #Only add if user wants to see charity items
                if (marked_for_charity == True):
                    if(see_charity == True):
                        return_data.append(hit["_source"])

                else:
                    #item is not marked for charity and can be added
                    return_data.append(hit["_source"])

        if (len(return_data) > TOTAL_REC_RETURN): 
            return return_data   

    return return_data 





def get_charity_value(elastic_client, userId):
    query = { 
        "query": {
            "bool": {
                "must": [
                    {   
                    "match": {"user_id": userId}
                    }
                ]
            } 
        }
    }

    response = elastic_client.search(index='user', body=query)
    hits = response["hits"]["hits"]

    #Format the search results to return as a JSON
    for hit in hits:
        #Ensures no duplicates are added
        user_data = hit["_source"]
        see_charity = user_data.get('charity') 

    return see_charity





def do_not_recommend_type(elastic_client, do_not_rec):

    do_not_show = do_not_rec
    titles = []
    
    #Get the titles of the do_not_rec listing based on Listing_ID
    for r in do_not_rec:
        query = { 
            "query": {
                "bool": {
                    "must": [
                        {   
                        "match": {"listing_id": r}
                        }
                    ]
                } 
            }
        }

        response = elastic_client.search(index='listing', body=query)
        hits = response["hits"]["hits"]

        #Format the search results to return as a JSON
        for hit in hits:
            #Ensures no duplicates are added
            listing_data = hit["_source"]
            titles.append(listing_data.get('title'))
            
    
    #Based on the title, get the top rec similar to this listing and add to do not recommend
    for t in titles:
        query = { 
            "size" : NUM_SIMILAR_RECS,
            "query": {
                "bool": {
                    "must": [
                        {   
                        "match": {"title": t}
                        }
                    ]
                } 
            }
        }

        response = elastic_client.search(index='listing', body=query)
        hits = response["hits"]["hits"]   

        count = 0
        #Format the search results to return as a JSON
        for hit in hits:
            if count < NUM_SIMILAR_RECS:
                listing_data = hit["_source"]
                do_not_show.append(listing_data.get('listing_id')) 
                count = count + 1
 
    return do_not_show


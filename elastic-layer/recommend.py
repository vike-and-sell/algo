from elasticsearch_dsl import Search
from update import *

## Recommend function called by app.py on reccomend request.
# returns a list of listings in JSON format
def recommend_algo(elastic_client, userId):
    print("recommending from Vike and sell..... ")

    ## Where the recommender magic will happen
    ## Preload with invalid data for the backend to compare against
    return_data = [] 
    
    # From the userId feild that was provided get the users search history from the elastic db
    search_history = get_search_history()
    # before looping through all search history results truncate it to the top 10 results
    for result in search_history:
        context = Search(using = elastic_client, index = "Listing") 
        s = context.query('query_string', query = result)
        response = s.execute() # This line is currently failing

        count = 0
        for hit in response:
            if count <= 5:
                return_data.append(hit)
                count = count + 1

    # This makes sure that if data is returned then it is a propper reccomendation
    # if False is returned then an error occured
    if return_data is not []:
        return return_data
    else:
        return False
    
def get_search_history():
    return["bike"]
    
def test_data():
    #Create test listing
    test_listing = { "SellerID": "User1", 
                    "ListingID": "1", 
                    "Title": "Blue Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    ID = test_listing.get('ListingID')
    #Add test listing to index listing
    add_doc("listing", ID, test_listing)

    #Create test listing
    test_listing = { "SellerID": "User2", 
                    "ListingID": "2", 
                    "Title": "Red Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    ID = test_listing.get('ListingID')
    #Add test listing to index listing
    add_doc("listing", ID, test_listing)

    #Create test listing
    test_listing = { "SellerID": "User3", 
                    "ListingID": "3", 
                    "Title": "Yellow Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    ID = test_listing.get('ListingID')
    #Add test listing to index listing
    add_doc("listing", ID, test_listing)

    #Create test listing
    test_listing = { "SellerID": "User4", 
                    "ListingID": "4", 
                    "Title": "Green Bike",  
                    "Description": "Very good bike", 
                    "Price": "20", 
                    "Location": "48.46, -123.31",  
                    "Status": "Available" }

    ID = test_listing.get('ListingID')
    #Add test listing to index listing
    add_doc("listing", ID, test_listing)

    test_user = {   "UserID": "User1",
                    "Location": "48.46, -123.31",
                    "Age": "20",
                    "SearchHistory": "Bike"
    }
    ID = test_user.get("UserID")
    add_doc("user", ID, test_user)

    test_user = {   "UserID": "User2",
                    "Location": "48.46, -123.31",
                    "Age": "20",
                    "SearchHistory": "Bike"
    }
    ID = test_user.get("UserID")
    add_doc("user", ID, test_user)

    test_user = {   "UserID": "User3",
                    "Location": "48.46, -123.31",
                    "Age": "20",
                    "SearchHistory": "Bike"
    }
    ID = test_user.get("UserID")
    add_doc("user", ID, test_user)

    test_user = {   "UserID": "User4",
                    "Location": "48.46, -123.31",
                    "Age": "20",
                    "SearchHistory": "Bike"
    }
    ID = test_user.get("UserID")
    add_doc("user", ID, test_user)

if __name__ == '__main__':
    test_data()
    recommend(1234)
# This file will contain the unit tests for the recomment.py file

def noSearchHistoryRecommendation():
    # Given a user
    # Get the recommendations for that user based on their search history
    # Since the user has no search history ensure that the results are the default values we want for a cold start
    # If they are the default results
        # Assert true
    # else
        # Assert False
    return False

def searchHistoryRecommendation():
    # Given a userId
    # Get the recommendations for that user based on their search history
        # Ensure that a testing user is used with a defined search history
    # Since the user has a defined search history, ensure that the results are what has been defined in the code
    # If the results are correct
        # Assert True
    # else
        # Assert False
    return False

def noDuplicateItemsInRecommendation():
    # Given a userId (with no search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs returned are the same

    # Given a userId (with a search history)
    # Get the recommendations for that user based on their search history
    # Assert that none of the listing IDs return are the same
    return False # No return should be needed depending on the testing framework used

def charityItemsFirst():
    # For a userId (with no search history)
    # Get the recommendation for that usesr
    # Assert that no charity listings are returned after the first non-charity listing

    # Repeete above for user with a search history
    return False
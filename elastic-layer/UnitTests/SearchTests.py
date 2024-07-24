# This file will contain the unit tests that will test the search.py functionality

def listingInDatabaseSearch():
    # using testing data loaded into the elastic database,
    # Preform a search for a specific item ie. "Bike"
    # and Assert that the listing returns the listing that is ensured to be in the database
    return False

def listingNotInDatabaseSearch():
    # knowing what testing data is loaded into the elastic database
    # Preform a search for a specific item ie. "Plane"
    # and Assert that no listings are returned
    return False

def addListingToDatabase():
    # Try adding a listing to the elastic database using the helper functions in app.py

    # at the end of this test remove the listing from the database so that the test remains self contianed
    return False

def modifyListingDetails():
    # Add a listing to the database 
    # Assert that it has been sucsessfully added to the data base

    # Attempt to modify the listing in the database

    # Remove the listing from the database to ensure the test remains self contained
    return False

def userInDatabaseSearch():
    # Given a user name contained in the testing data
    # Preform a search for that user
    # Assert that the userId returned matches that of the corresponding user name in the testing data
    return False

def userNotInDatabaseSearch():
    # Given a user name not contained in the testing data
    # preform a search for that user
    # Assert that no user is returned
    return False

def addAndRemoveUserElasticDB():
    # Using the helper functions in app.py
    # add a user to the database
    # preform a search for that user and ensure that they have sucsessfuly been added
    # Remove that user from the database to ensure the test remains self contained
    # preform a search for 
    return False

def modifyUserDetails():
    # add a user to the elastic db
    # preform a search for the user and ensure that the object returned is the same as the one added
    # Modify the user using the helper functions in app.py
    # preform a search for the user and ensure that the object returned is not the same as the one added
    # Remove the user from the database to ensure the test remains self contained
    return False

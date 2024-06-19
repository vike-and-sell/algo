-- create_tables_and_insert_data.sql
CREATE EXTENSION cube;
CREATE EXTENSION earthdistance;

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE CHECK (username ~ '^[a-zA-Z0-9_@]{6,20}$'),
    email VARCHAR(100) NOT NULL UNIQUE CHECK (email ~ '^[^@]+@uvic\.ca$'),
    password VARCHAR(100) NOT NULL CHECK (password ~ '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$'),
    location EARTH NOT NULL,
    address VARCHAR(100) NOT NULL,
    joining_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    items_sold INT[] NOT NULL DEFAULT '{}',
    items_purchased INT[] NOT NULL DEFAULT '{}'
);

-- Create Listings table
CREATE TABLE IF NOT EXISTS Listings (
    listing_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL REFERENCES Users(user_id),
    title VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    location EARTH NOT NULL,
    address VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('AVAILABLE', 'SOLD', 'REMOVED')),
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create Listing Ratings table
CREATE TABLE IF NOT EXISTS Listing_Ratings (
    listing_rating_id SERIAL PRIMARY KEY,
    rated_listing_id INT NOT NULL REFERENCES Listings(listing_id),
    rating_user_id INT NOT NULL REFERENCES Users(user_id),
    rating_value INT NOT NULL CHECK (rating_value BETWEEN 1 AND 5),
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create Listing Reviews table
CREATE TABLE IF NOT EXISTS Listing_Reviews (
    listing_review_id SERIAL PRIMARY KEY,
    reviewed_listing_id INT NOT NULL REFERENCES Listings(listing_id),
    review_user_id INT NOT NULL REFERENCES Users(user_id),
    review_content TEXT NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy data into Users table
INSERT INTO Users (username, email, password, location, address, joining_date)
VALUES
('john_doe', 'john_doe@uvic.ca', 'Password123!',  ll_to_earth(34.052235,118.243683), '123 Valley Lane', '2023-01-01'),
('jane_smith', 'jane_smith@uvic.ca', 'SecurePass1$',  ll_to_earth(34.052235,-118.243683), '842 Boniface Dr', '2023-02-01'),
('ann_lawson', 'ann_law@uvic.ca', 'Password1234!',  ll_to_earth(48.468997, -123.329709) '1660 Mckenzie Ave', '2023-05-01');

-- Insert dummy data into Listings table
INSERT INTO Listings (seller_id, title, price, location, address, status)
VALUES
(1, 'Bicycle for sale', 150.00, ll_to_earth(40.730610,-73.935242), '440 Kilner St', 'AVAILABLE'),
(2, 'Laptop for sale', 800.00, ll_to_earth(34.052235,-118.243683), '892 Jonas Ave', 'AVAILABLE');

-- Insert dummy data into Listing Ratings table
INSERT INTO Listing_Ratings (rated_listing_id, rating_user_id, rating_value, created_on)
VALUES
(1, 2, 4, '2023-03-03 12:00:00'),
(2, 1, 5, '2023-04-03 17:45:00');

-- Insert dummy data into Listing Reviews table
INSERT INTO Listing_Reviews (reviewed_listing_id, review_user_id, review_content, created_on)
VALUES
(1, 2, 'The bicycle was in excellent condition, very happy with the purchase!', '2023-03-03 12:05:00'),
(2, 1, 'The laptop works perfectly, very satisfied!', '2023-04-03 17:50:00');

-- TODO: add table that includes information on clicks, search history, and blocked recommendations
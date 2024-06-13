CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    location TEXT NOT NULL,
    join_date TIMESTAMP NOT NULL,
    items_sold INTEGER[] NOT NULL,
    items_purchased INTEGER[] NOT NULL,
    profile_picture TEXT,
    biography TEXT
);

INSERT INTO Users (username, email, password, location, join_date, items_sold, items_purchased, profile_picture, biography) 
VALUES 
    ('john_doe', 'john@example.com', 'password123', 'New York', '2024-06-10 12:00:00', '{101, 102}', '{201, 202}', 'profile_pics/john.jpg', 'I love selling and buying cool stuff!'),
    ('jane_smith', 'jane@example.com', 'securepass', 'Los Angeles', '2024-06-10 11:30:00', '{103}', '{203, 204}', 'profile_pics/jane.jpg', 'Fashion enthusiast and seller!'),
    ('sam_jackson', 'sam@example.com', 'samspassword', 'Chicago', '2024-06-09 10:45:00', '{104, 105}', '{205}', 'profile_pics/sam.jpg', 'Passionate about technology and gadgets.');
-- Database Schema Generation for HBnB Project

-- 1. Create User Table
CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 2. Create Place Table
CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- 3. Create Review Table
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_place_review UNIQUE (user_id, place_id)
);

-- 4. Create Amenity Table
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- 5. Create Place_Amenity Junction Table
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- Initial Data Insertion

-- Insert Administrator User
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$e8pA1.m1P7L4mGZ9fO7D.e4R1J.G2z8Y3X4W5V6U7T8S9R0Q1P2O3',
    TRUE
);

‏-- Insert Initial Amenities
‏INSERT INTO Amenity (id, name) VALUES
‏('a4f4ba51-47d7-4b98-909b-b3299d3f337b', 'WiFi'),
‏('b7414fca-29de-4519-a225-03631afbc6c6', 'Swimming Pool'),
‏('8e460f6a-6fd3-4794-8859-240fa58a9958', 'Air Conditioning');

-- Testing CRUD Operations

-- CREATE Test: Insert a sample user and place
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('d4e5f6a7-b8c9-40d1-e2f3-445566778899', 'John', 'Doe', 'john@example.com', 'hashed_pass_123', FALSE);

INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES ('e5f6a7b8-c9d0-41e2-f3a4-556677889900', 'Cozy Apartment', 'Nice stay in downtown', 150.00, 24.7136, 46.6753, 'd4e5f6a7-b8c9-40d1-e2f3-445566778899');

-- READ Test: Retrieve admin user and created place
SELECT * FROM User WHERE is_admin = TRUE;
SELECT * FROM Place WHERE owner_id = 'd4e5f6a7-b8c9-40d1-e2f3-445566778899';

-- UPDATE Test: Update place price
UPDATE Place SET price = 175.00 WHERE id = 'e5f6a7b8-c9d0-41e2-f3a4-556677889900';

-- DELETE Test: Delete sample place
DELETE FROM Place WHERE id = 'e5f6a7b8-c9d0-41e2-f3a4-556677889900';
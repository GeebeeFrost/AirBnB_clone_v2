-- This script prepares a MySQL server for the project

-- Create the hbnb_test_db database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the hbnb_test user with a secure password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the hbnb_test_db database to the hbnb_test user
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to the hbnb_test user
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';

-- Refresh privileges to ensure the changes take effect
FLUSH PRIVILEGES;


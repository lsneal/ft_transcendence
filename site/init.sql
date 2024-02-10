DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    user_email VARCHAR(255) UNIQUE NOT NULL,
    user_first_name VARCHAR(20) NOT NULL,
    user_last_name VARCHAR(20) NOT NULL,
    user_birthdate DATE NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modification_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    insertion_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users(
    username,
    user_email,
    user_first_name,
    user_last_name,
    user_birthdate
)
VALUES 
    ('cwenga','cwenga@carml.ai','carmel','wenga','1990-09-20'),
    ('smenguope','smenguope@carml.ai','suzie','menguope','1992-11-13'),
    ('cdiogni','cdiogni@carml.ai','christian','diogni','1992-10-13');


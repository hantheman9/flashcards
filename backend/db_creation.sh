#!/bin/bash

# Database connection parameters
host="xx.xx.xx.xx"
dbname="flashcardsdb"
user="flashcardsapp"
password="XXXXXXXXXX"

# Use PGPASSWORD environment variable to supply the password to psql
export PGPASSWORD=$password
# Connect to the database and execute the SQL statement
psql -h $host -U $user -d $dbname -c "DROP TABLE IF EXISTS flashcard;"
psql -h $host -U $user -d $dbname -c 'DROP TABLE IF EXISTS "user";'
psql -h $host -U $user -d $dbname -c 'CREATE TABLE "user" (id SERIAL PRIMARY KEY,username VARCHAR(120) NOT NULL UNIQUE,email VARCHAR(120) NOT NULL UNIQUE, password_hash VARCHAR(256) NOT NULL UNIQUE);'
psql -h $host -U $user -d $dbname -c 'CREATE TABLE flashcard (id SERIAL PRIMARY KEY,word VARCHAR(120) NOT NULL,definition TEXT NOT NULL,bin INTEGER DEFAULT 0,next_review_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,incorrect_count INTEGER DEFAULT 0,user_id INTEGER,FOREIGN KEY (user_id) REFERENCES "user"(id));'



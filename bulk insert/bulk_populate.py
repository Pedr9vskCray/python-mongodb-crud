from dotenv import load_dotenv, find_dotenv # framework for working with environment variables
from pymongo import MongoClient
from datetime import datetime as dt
import os
import pprint

# loading environment variables
load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")

# connection string

connection_string = f"mongodb+srv://{username}:{password}@clusterdemo.mjzcowt.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDemo&authSource=admin"

# connecting

client = MongoClient(connection_string)

# connecting to the production database

production = client.production

# inserting data into the authors collection

def populate_data_authors():
    authors = [
        {
            "first_name": "George",
            "last_name": "Orwell",
            "date_of_birth": dt(1903, 6, 25) # using the datetime constructor to create a date
        },
        {
            "first_name": "Agatha",
            "last_name": "Christie",
            "date_of_birth": dt(1890, 9, 15)
        },
        {
            "first_name": "Pedro",
            "last_name": "Lobão",
            "date_of_birth": dt(2005, 2, 21)
        },
        {
            "first_name": "Herman",
            "last_name": "Melville",
            "date_of_birth": dt(1819, 8, 1)
        },
        {
            "first_name": "F. Scott",
            "last_name": "Fitzgerald",
            "date_of_birth": dt(1896, 9, 24)
        }
    ]

    # inserting the data to our authors collection

    author_collection = production.author

    authors_ids = author_collection.insert_many(authors).inserted_ids

    return authors_ids

    # now, since we need to create the authors first and the books after
    # we'll run this function inside the populate_data_books() function
    # and since this function returns all the ids of the authors we've just inserted
    # we can use this information to populate our book collection and create relationships

# inserting data into the book collection

def populate_data_books():

    authors_ids = populate_data_authors()

    books = [
        {
            "title": "1984",
            "authors": [authors_ids[0]],
            "publish_date": dt(1964, 6, 8),
            "type": "Fiction",
            "copies": 30000000
        },
        {
            "title": "And Then There Were None",
            "authors": [authors_ids[1]],
            "publish_date": dt(1939, 11, 6),
            "type": "Fiction",
            "copies": 100000000
        },
        {
            "title": "MongoDB with Python",
            "authors": [authors_ids[2]],
            "publish_date": dt(2025, 4, 1),
            "type": "Non-Fiction",
            "copies": 1
        },
        {
            "title": "Moby Dick",
            "authors": [authors_ids[3]],
            "publish_date": dt(1851, 10, 18),
            "type": "Fiction",
            "copies": 500000000
        },
        {
            "title": "The Great Gatsby",
            "authors": [authors_ids[4]],
            "publish_date": dt(1925, 4, 10),
            "type": "Fiction",
            "copies": 25000000
        },
        {
            "title": "Learn Django/Flask Fast",
            "authors": [authors_ids[2]],
            "publish_date": dt(2025, 2, 21),
            "type": "Non-Fiction",
            "copies": 1
        }
    ]

    # inserting our books to our book collection

    book_collection = production.book

    book_collection.insert_many(books)

# now we'll run the function for inserting the books which will run the other function for the authors

populate_data_books()
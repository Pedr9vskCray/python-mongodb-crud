from dotenv import load_dotenv, find_dotenv # framework for working with environment variables
from pymongo import MongoClient
import os
import pprint

# loading environment variables
load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")

# connection string

connection_string = f"mongodb+srv://{username}:{password}@clusterdemo.mjzcowt.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDemo"

# connecting

client = MongoClient(connection_string)

# access database

test_dbs = client.test

# create document function

def insert_test_document():
    collection = test_dbs.test # accessing the test collection in the test database
    test_document = {
        "name": "Pedro José",
        "type": "male human"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)

#insert_test_document()
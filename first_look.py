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

# list database

dbs = client.list_database_names()
print(dbs)

# access database
# foo = client.<database_name> or client["<database_name>"]

test_dbs = client.test

# accessing collections in a database

collections = test_dbs.list_collection_names()
print(collections)
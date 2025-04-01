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

# connecting to the production database

production = client.production

# accessing the person_collection

person_collection = production.person_collection

# delete document by id

def delete_by_id(personid: str):
    from bson.objectid import ObjectId

    _id = ObjectId(personid)

    person_collection.delete_one({"_id": _id})

#delete_by_id("67ea8c3d6426dd4445249d1e")

# delete many documents

def delete_many():
    person_collection.delete_many({})
    # similar to when querying data, you can select specific conditions for you delete

#delete_many()
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

# relating documents by embedding them together

def add_address_embed(personid: str, address: dict):
    from bson.objectid import ObjectId

    _id = ObjectId(personid)

    person_collection.update_one({"_id": _id}, {"$addToSet": {"addresses": address}})
    # "$addToSet" -> adds a value to an array unless the value is already present, 
    # in which case does nothing. If the array doesn't exist, it creates it.

address = {
    "_id": "46ae4d1e2626ee2465571d28",
    "street": "Bay Street",
    "number": 2706,
    "city": "San Francisco",
    "country": "United States",
    "zip": "94107"
}

#add_address_embed("67ea8c3d6426dd4445249d20", address)

# relating documents by owner_id

def add_address_relationship(personid: str, address: dict):
    from bson.objectid import ObjectId

    _id = ObjectId(personid)

    # adding owner_id field to the address received as a function parameter

    address = address.copy()
    address["owner_id"] = personid

    # creating a new collection for our addresses

    address_collection = production.addresses

    # inserting the address we have to the collection we just created

    address_collection.insert_one(address)

#add_address_relationship("67ea8c3d6426dd4445249d1c", address)
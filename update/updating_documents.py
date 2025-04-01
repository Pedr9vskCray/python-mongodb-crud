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

# updating person by id

def update_by_id(personid: str):
    from bson.objectid import ObjectId

    _id = ObjectId(personid)

    updates = {
        "$set": {"new_Field": True}, # "$set" -> adds a new or overrides an existing field
        "$inc": {"age": 1}, # "$inc" -> increments the value on the specified field
        "$rename": {"first_name": "f_name", "last_name": "l_name"},
        # "$rename" -> rename the specified field (it renames the field name, not the value!)
        "$currentDate": {"today": { "$type": "date" }}
        # "$currentDate" -> sets the specified field to receive today's date
    }

    person_collection.update_one({"_id": _id}, updates)

#update_by_id("67ea8c3d6426dd4445249d1e")

# unseting a field

def unset_by_id(personid: str):
    from bson.objectid import ObjectId

    _id = ObjectId(personid)

    person_collection.update_one({"_id": _id}, {"$unset": {"new_Field": ""}})
    # "$unset" -> deletes/unsets the specified field, which in turn deletes the value

#unset_by_id("67ea8c3d6426dd4445249d1e")

# replacing a document

# replacing a document can be useful when wanting to change all the information related to said
# document but keeping its id the same as before

def replace_one(personid: str):
    from bson.objectid import ObjectId

    _id = ObjectId(personid)

    new_document = {
        "first_name": "Isabela",
        "last_name": "Rosa",
        "age": 27
    }

    person_collection.replace_one({"_id": _id}, new_document)

#replace_one("67ea8c3d6426dd4445249d1f")
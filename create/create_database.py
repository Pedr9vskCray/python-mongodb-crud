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

# creating a production database
# when trying to access a database that don't exist, mongodb automatically creates that database

production = client.production

# creating a collection inside that database
# when trying to access a collection that don't exist, mongodb automatically creates that collection

person_collection = production.person_collection

# inserting documents in the collection
# when creating a database and collection from scratch like we're doing here, you need to insert a
# document with it or else the database and collection won't actually be created

def insert_documents():
    first_name = ['Pedro', 'João', 'Felipe', 'Maria', 'Julia']
    last_name = ['José', 'Joaquim', 'Machado', 'Joaquina', 'Amorim']
    ages = [25, 19, 28, 32, 17]

    documents = []

    for fname, lname, age in zip(first_name, last_name, ages):
        document = {
            "first_name": fname,
            "last_name": lname,
            "age": age
        }
        documents.append(document)
        #person_collection.insert_one(document)

    inserted_ids = person_collection.insert_many(documents).inserted_ids
    print(inserted_ids)

#insert_documents()
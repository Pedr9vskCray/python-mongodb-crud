from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import os
from pprint import PrettyPrinter

# setting up our printer

printer = PrettyPrinter()

# loading environment variables
load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")

# connection string

connection_string = f"mongodb+srv://{username}:{password}@clusterdemo.mjzcowt.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDemo&authSource=admin"

# connecting

client = MongoClient(connection_string)

# connecting to the database

jeopardy_db = client.jeopardy_db

# accessing the question collection

question_coll = jeopardy_db.question

# now we repeat the same function as before but we add a new synonyms parameter

def fuzzy_matching():
    result = question_coll.aggregate([
        {
            "$search": {  # operator for full-text search
                "index": "language_search",  # the index we've created for our collection
                "text": {
                    "query": "beer", # what we want to search for
                    "path": "category", # field where we want to search on
                    "synonyms": "mapping"
                }
            }
        }
    ])
    
    for match in list(result):
        printer.pprint(match)
        print('\n')

fuzzy_matching()

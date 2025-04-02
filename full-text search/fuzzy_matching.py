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

# after indexing the data in our collection, we can use the index we set up to perform searches

def fuzzy_matching():
    result = question_coll.aggregate([
        {
            "$search": {  # operator for full-text search
                "index": "language_search",  # the index we've created for our collection
                "text": {
                    "query": "computer", # what we want to search for
                    "path": "category", # field where we want to search on
                    "fuzzy": {} # precision on our fuzzy search, for now we'll use the default parameters
                }
            }
        }
    ])
    for match in list(result):
        printer.pprint(match)
        print('\n')

fuzzy_matching()

# for a more exact search we can do the same thing but remove the "fuzzy" parameter
# which will lend us results containing exactly what we've put in our "query" parameter

# "text", "fuzzy" and synonyms documentation:
# https://www.mongodb.com/pt-br/docs/atlas/atlas-search/text/
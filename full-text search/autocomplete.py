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

# now we'll set up a search that will gives us autocomplete results similar to how google works
# first step is to remove the synonyms we've added previously because autocomplete is not supported with the json editor
# after that we'll add a field mapping on the "question" field and the data type as autocomplete

# autocomplete properties:

# analyzer: lucene.standard
# max grams: 15
# min grams: 2
# tokenization: edgeGram
# fold diacritics: true

# writing the autocomplete function

def autocomplete():
    result = question_coll.aggregate([
        {
            "$search": {
                "index": "language_search",
                "autocomplete": { # instead of text we're using autocomplete
                    "query": ["computer programmer"],
                    "path": "question", # field we added in our field mapping
                    "tokenOrder": "sequential", # wether or not we're look for something sequential
                    "fuzzy": {}
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "question": 1
            }
        }
    ])

    for quest in list(result):
        printer.pprint(quest)

# "tokenOrder": "sequential" means we're looking for this specific order of words in our questions
# "tokenOrder": "any" means we're looking for these words in any order they may appear

# autocomplete documentation:
# https://www.mongodb.com/pt-br/docs/atlas/atlas-search/autocomplete/

autocomplete()
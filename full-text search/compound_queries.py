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

# another way to do queries in mongodb is by using compound queries
# this is another advanced way of narrowing down our search query
# using operators to filter out specific results or prioritize specific results

def compound_queries():
    result = question_coll.aggregate([
        {
            "$search": {
                "index": "language_search",
                "compound": {
                    "must": [ # the category must include "computer" or "coding" 
                        {
                            "text": {
                                "query": ["COMPUTER", "CODING"],
                                "path": "category",
                            }
                        }
                    ],
                    "mustNot": [ # the category must not include "codes"
                        {
                            "text": {
                                "query": "codes",
                                "path": "category"
                            }
                        }
                    ],
                    "should": [ # the answer should include "application", prioritizing returning those who have it
                        {
                            "text": {
                                "query": "application",
                                "path": "answer"
                        }
                        }
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "questions": 1,
                "answer": 1,
                "category": 1,
                "score": {"$meta": "searchScore"} # a score that determines on how well our result matched our search
            }
        }
    ])

    for data in list(result):
        printer.pprint(data)
        print('\n')

compound_queries()

# compound queries documentation:
# https://www.mongodb.com/pt-br/docs/atlas/atlas-search/compound/
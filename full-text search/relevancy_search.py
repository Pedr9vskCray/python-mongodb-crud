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

# relevancy search is a compound search in which you boost the score of specific results if they
# match your desired parameter, prioritizing results based on their score, focusing on matching your standards

def relevancy_search():

    result = question_coll.aggregate([
        {
            "$search": {
                "index": "language_search",
                "compound": {
                    "must": [
                        {
                            "text": {
                                "query": "computer",
                                "path": "category"
                            }
                        }
                    ],
                    "should": [
                        {
                            "text": {
                                "query": "Final Jeopardy",
                                "path": "round",
                                "score": {"boost": {"value": 3.0}} # multiplies the score of results that have this query in the "round" field
                            }
                        },
                        {
                            "text": {
                                "query": "Double Jeopardy",
                                "path": "round",
                                "score": {"boost": {"value": 2.0}} # multiplies the score of results that have this query in the "round" field
                            }
                        }
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "question": 1,
                "answer": 1,
                "category": 1,
                "round": 1,
                "score": {"$meta": "searchScore"}
            }
        },
        {
            "$limit": 10 # result quantity is limited to 10
        }
    ])

    for data in list(result):
        printer.pprint(data)
        print('\n')


relevancy_search()

# relevancy search documentation:
# https://www.mongodb.com/pt-br/docs/atlas/atlas-search/scoring/
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import os
import pprint
import json

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

# reading the first 10k questions

jeopardy_questions = []

with open("JEOPARDY_QUESTIONS1.json", "r") as questions:
    data = json.load(questions)
    for question in range(10000, 100000):
        jeopardy_questions.append(data[question])

# inserting the documents in the question collection

def insert_documents(docs: list):
    inserted_ids = question_coll.insert_many(docs).inserted_ids
    print(inserted_ids)

#insert_documents(jeopardy_questions)

# the .json file used for this insert can be found here:
# https://domo-support.domo.com/s/article/360043931814?language=en_US
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

# connecting to our jeopardy_db database

jeopardy_db = client.jeopardy_db

# creating our synonym collection

synonym = jeopardy_db.synonym

# inserting documents to actually create the collection

synonyms_equivalent = {
    "mappingType": "equivalent", "synonyms": ["computer", "laptop", "tech"]
}

# when creating synonyms in the "equivalent" mappingType, all words are synonyms to each other
# so if we seach for "laptop" we'll also receive results for "computer" and "tech" and vice-versa

synonyms_explicit = {
    "mappingType": "explicit",
    "input": ["beer"],
    "synonyms": ["brew", "pint"]
}

# when creating synonyms in the "explicit" mappingType, only the input word is synonym to the others
# so if we search for "beer" we'll also receive results for "brew" and "pint"
# but if we search for "pint" we'll not receive results for neither "beer" nor "brew" 

# inserting our synonyms in our synonym collection

def insert_document(doc: dict):
    inserted_id = synonym.insert_one(doc).inserted_id
    print(inserted_id)

#insert_document(synonyms_equivalent)
#insert_document(synonyms_explicit)

# now we need to use the json editor to edit our search index to look something like this

{
  "analyzer": "lucene.english",
  "searchAnalyzer": "lucene.english",
  "mappings": {
    "dynamic": true
  },
  "synonyms": [
    {
      "analyzer": "lucene.english",
      "name": "mapping",
      "source": {
        "collection": "synonym"
      }
    }
  ]
}
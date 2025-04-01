from dotenv import load_dotenv, find_dotenv # framework for working with environment variables
from pymongo import MongoClient
import os
import pprint

# loading environment variables
load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")

# connection string

connection_string = f"mongodb+srv://{username}:{password}@clusterdemo.mjzcowt.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDemo&authSource=admin"

# connecting

client = MongoClient(connection_string)

# connecting to the production database

production = client.production

# setting up the schema validation and creating the book collection

def create_book_collection():

    book_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "authors", "publish_date", "type", "copies"],
            "properties": {
                "title": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "authors": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId",
                        "description": "must be an objectId and is required"
                    }
                },
                "publish_date": {
                    "bsonType": "date",
                    "description": "must be a date and is required"
                },
                "type": {
                    "enum": ["Fiction", "Non-Fiction"],
                    "description": "can only be one of those enum values and is required"
                },
                "copies": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be an integer greater than 0 and is required"
                }
            }
        }
    }

    # keyword documentation
    # https://www.mongodb.com/pt-br/docs/manual/reference/operator/query/jsonSchema/#std-label-jsonSchema-keywords

    # now we'll create the collection that will hold our book schema

    try:
        production.create_collection("book")
    except Exception as error:
        print(error)

    # now we'll add the schema validator to our new collection

    
    production.command("collMod", "book", validator=book_validator)
    # "collMod" is a command in the mongodb syntax that lets you modify collections
    # so we're modifying the collection "book" by adding a validator to it

# setting up the schema validation and creating the author collection

def create_author_collection():

    author_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "first_name",
                "last_name",
                "date_of_birth"
            ],
            "properties": {
                "first_name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "last_name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "date_of_birth": {
                    "bsonType": "date",
                    "description": "must be a date and is required"
                }
            }
        }
    }

    # creating our author collection
    
    try:
        production.create_collection("author")
    except Exception as error:
        print(error)

    # adding our schema validator to our author collection

    production.command("collMod", "author", validator=author_validator)

# calling both functions and analyzing its behaviour

create_book_collection()
create_author_collection()
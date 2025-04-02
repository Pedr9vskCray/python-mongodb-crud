from dotenv import load_dotenv, find_dotenv # framework for working with environment variables
from pymongo import MongoClient
from datetime import datetime as dt
import pyarrow
from pymongoarrow.api import Schema
from pymongoarrow.monkey import patch_all
import os
import pprint
import pymongoarrow as pma
from bson import ObjectId
import pandas as pd
import numpy as np

# defining a printer

printer = pprint.PrettyPrinter()

# running patch_all() to ensure connection between pymongoarrow and the collections

patch_all()

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

# defining collections

author_coll = production.author
book_coll = production.book

# defining our schema

# our schema is defining which fields from our collection will be present on our dataframe
# any field not specified here will not be included
# any field that was specified but its not in any of the documents in the collection will be None or NULL

author = Schema({
    "_id": ObjectId,
    "first_name": pyarrow.string(),
    "last_name": pyarrow.string(),
    "date_of_birth": dt
})

# reading our collection as a pandas dataframe

df = author_coll.find_pandas_all({}, schema=author)
print(df.head())

print('\n')

# reading our collection as a arrow table

arrow_table = author_coll.find_arrow_all({}, schema=author)
print(arrow_table)

print('\n')

# reading our collection as numpy array

ndarrays = author_coll.find_numpy_all({}, schema=author)
print(ndarrays)

print('\n')

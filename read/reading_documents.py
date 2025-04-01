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

# connecting to the production database

production = client.production

# accessing the person_collection

person_collection = production.person_collection

# querying data from the collection

printer = pprint.PrettyPrinter() # using the pprint framework for better print output

def find_all_people():
    # finding all the documents in this collection
    people = person_collection.find()
    # in this case, person becomes a cursor object containing all the data we've queried
    # similar to cursor objects in rdbs we can iterate through the cursor to view our data

    # print(people) -> cursor object
    # print(list(people)) -> receive all the elements from it at once

    for person in people:
        printer.pprint(person)
        print('\n')

find_all_people() 

# data extracted this way can be used inside the code just like a python dictionary

# now we can look on how to extract especific data based on field values

def find_pedro():
    pedro = person_collection.find_one({"first_name": "Pedro", "age": 25})
    printer.pprint(pedro)
    print('\n')

find_pedro()

# counting the number of documents inside our collection

def count_all():
    count = person_collection.count_documents(filter={})
    # another way to count is by adding the .count() to the end of the query
    # people = person_collection.find().count()
    print("Number of people in the database: ", count)
    print('\n')

count_all()

# now we'll write a function to find a person by its id
# to search for documents by id, you cannot simply copy and paste it into the find() function
# because when an id is returned by mongodb and it comes into python, it becomes a string object
# to search by an id, the id itself needs to be this special type called ObjectId and not a string
# so to transform the string into the type we need, we can use the bson framework

def find_by_id(person_id: str):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id": _id})

    printer.pprint(person)
    print('\n')

find_by_id("67ea8c3d6426dd4445249d1e")

# finding people by an age range

def find_age_range(min_age: int, max_age: int): 
    query = {
        "$and": [
            {"age": {"$gte": min_age}}, # gte -> greater than or equal to
            {"age": {"$lte": max_age}}  # lte -> less than or equal to
        ]
    }
    
    # query sintax -> find all documents where (age >= min_age and age <= max_age)
    people = person_collection.find(query).sort("age") # sorting by a especific field
    for person in people:
        printer.pprint(person)
        print('\n')

find_age_range(18, 30)

# extracting only wanted information

def project_columns():
    columns = {"_id": 0, "first_name": 1, "last_name": 1}
    # "_id" = 0 means we don't want the id field in our query
    # also not specifying the age field, automatically removes it from the query aswell
    people = person_collection.find({}, columns).sort("age")
    # we can still sort by age even though we don't want it in our query result

    for person in people:
        printer.pprint(person)
        print('\n')

project_columns()
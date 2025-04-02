from dotenv import load_dotenv, find_dotenv # framework for working with environment variables
from pymongo import MongoClient
from datetime import datetime as dt
import os
import pprint

# defining a printer

printer = pprint.PrettyPrinter()

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

# find and return all the books that contain the letter "a"

def find_books_by_letter():

    book_collection = production.book

    book_with_a = book_collection.find(
        {"title": {"$regex": "a{1}", "$options": "i"}} # regular expressions similar to python
        )

    for book in list(book_with_a):
        printer.pprint(book)
        print('\n')

find_books_by_letter()

# operators documentation
# https://www.mongodb.com/pt-br/docs/manual/reference/operator/

# doing a join operation to grab every author and every book they wrote embedded inside the author

def authors_and_books():

    author_collection = production.author

    authors_and_books = author_collection.aggregate([{
        "$lookup": { # "$lookup" performs a left outer join with any collection in the same database
            "from": "book",
            "localField": "_id", # field on the author collection we're going to perform the join with
            "foreignField": "authors", # field on the book collection we're going to perform the join with
            "as": "books" # name of the field added to author that contains all of the books resulted from the join
        }
    }])

    # mongodb automatically handles the list of authors in each book so we don't have to worry

    # recapping, we're performing a left outer join on the author collection with the book collection
    # where we're going to match them by the author "_id" field and the book "authors" field, and since
    # this is a left outer join the result will only contain books that have an author in the author collection
    # but can return authors that have no books related to their "_id"

    for info in list(authors_and_books):
        printer.pprint(info)
        print('\n')

authors_and_books()

# now we'll add a new field containing how many books each author wrote

def author_books_count():

    author_collection = production.author

    author_and_books_count = author_collection.aggregate([
        {
            "$lookup": {
                "from": "book",
                "localField": "_id",
                "foreignField": "authors",
                "as": "books"
            }
        },
        {
            "$addFields" : { 
                "total_books": {"$size": "$books"} 
            }
        },
        {
            "$project": {
                "first_name": 1,
                "last_name": 1,
                "total_books": 1,
                "_id": 0
            }
        }
    ])

    # so here we're adding a new field to out query result (which includes the join on authors and books)
    # the field name is "total_books" and its value will be the size of the books field we've just created in the join (for each author!)
    # basically we're storing all the books each author wrote and how many of those books there are
    # after that we'll filter which fields we want in our query result by using "$project"

    # you can view this operation sequence as a cascade operation, where the last operation will be performed
    # on the result of the operation before it: "$lookup" <- "$addFields" <- "$project"

    for info in list(author_and_books_count):
        printer.pprint(info)
        print('\n')

author_books_count()

# now we'll grab the authors and books but only for authors of a certain age

def books_old_authors():

    book_collection = production.book

    books_with_old_authors = book_collection.aggregate([
        {
            "$lookup": {
                "from": "author",
                "localField": "authors",
                "foreignField": "_id",
                "as": "authors"
            }
        },
        {
            "$set": { # "$set" overrides the value in the field or creates a new field if it doesn't exist
                "authors": {
                    "$map": { # "$map" applies an expression to each element in an array and returns an array with the applied results
                        "input": "$authors", # the input array for "$map" is referenced in "$authors"
                        "in": { # what we want inside each element that's inside the array returned by "$map"
                            "age": { 
                                "$dateDiff": { # difference between 2 dates
                                    "startDate": "$$this.date_of_birth", # "$$this." references the current author we're iterating over with "$map"
                                    "endDate": "$$NOW", # "$$NOW" is today's date
                                    "unit": "year" # shows the unit of precision, in this case we only care about the year
                                }
                            },
                            "first_name": "$$this.first_name",
                            "last_name": "$$this.last_name"
                        }
                    }
                }
            }
        },
        {
            "$match": { # "$match" filters data through a logic operation and keep those that return True
                "$and": [ # if (authors.age >= 50 and authors.age <= 150) return True; else False.
                    {"authors.age": {"$gte": 50}},
                    {"authors.age": {"$lte": 150}}
                ]
            }
        },
        {
            "$sort": { # "$sort" sorts by an specified field (1: ASC, -1: DESC)
                "age": 1
            }
        }
    ])

    # what "$map" is doing is basically iterating over an existing array and returning a new array
    # in which each element of this new array comes from transformed information received through the iteration
    # this new array replaces the old one as indicated by the "$set"

    for info in list(books_with_old_authors):
        printer.pprint(info)
        print('\n')

books_old_authors()

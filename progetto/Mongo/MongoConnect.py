
import pymongo as pymongo
from random import randrange

# serviva: pip3 install pymongo[srv] oltre l'import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("MONGODB_ATLAS_CLUSTER_URI")
    x = client.list_database_names()
    collection = client.test['quotes']

    author = "gandhi"
    category = "any"

    # search quotes just for category by any author
    if author == "any" and category != "any":
        items = list(collection.find({"Category": category}))
    # search quotes by author or part of an author's name for any category
    elif author != "any" and category == "any":
        items = list(collection.find({"Author": {'$regex': author, '$options': 'i'}}))
    # search quotes by any author for not formatted categories
    elif author == "any" and category == "any":
        items = list(collection.find({'$or': [{"Category": "quotes"}, {"Category": ""}]}))
    # search quotes having both category and author
    else:
        items = list(collection.find({"Category": category, "Author": {'$regex': author, '$options': 'i'}}))

    lenQuotes = len(items)

    if lenQuotes == 0:
        print("No quotes!")
    if lenQuotes == 1:
        index = 0
    else:
        index = randrange(lenQuotes)

    stringa = str(items[index]['Quote']) + " by " + str(items[index]['Author'])
    print(stringa)

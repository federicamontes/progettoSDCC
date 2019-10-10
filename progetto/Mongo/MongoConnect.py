import pymongo as pymongo


# serviva: pip3 install pymongo[srv] oltre l'import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongoAtlas_uri")
    x=client.list_database_names()
    db = client.test
    collection = db['quotes']
    cursor = collection.find({})
    print(cursor.count())
    #for document in cursor:
    #    print(document)



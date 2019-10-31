import pymongo as pymongo
from random import randrange
import os
import json
import boto3
import time
import csv
import sys




def call_to_Tagslambda(category, author):
    # lambda_client = boto3_client('lambda')

    sns = boto3.client ('sns')

    msg = {"Category": category, "Author": author}

    response = sns.publish (
        TopicArn=os.environ["SNS_TOPIC_ARN"],
        Message=json.dumps (msg))

    # print("response: " + str(response['Attributes']))
    print ("response: " + str (json.dumps (msg)) + str (response))
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return "Loading... :D"


# always start with the lambda_handler
def getQuote(category, author):
    # connection to MongoAtlas
    client = pymongo.MongoClient(os.environ["MONGODB_ATLAS_CLUSTER_URI"])
    collection = client.test['quotes']

    # search quotes just for category by any author
    if author == "any" and category != "any":
        items = list (collection.find ({"Category": category}))
    # search quotes by author or part of an author's name for any category
    elif author != "any" and category == "any":
        items = list (collection.find ({"Author": {'$regex': author, '$options': 'i'}}))
    # search quotes by any author for not formatted categories
    elif author == "any" and category == "any":
        items = list (collection.find ({'$or': [{"Category": "quotes"}, {"Category": ""}]}))
    # search quotes having both category and author
    else:
        items = list (collection.find ({"Category": category, "Author": {'$regex': author, '$options': 'i'}}))

    lenQuotes = len (items)
    if lenQuotes == 0:
        return call_to_Tagslambda (category, author)
    if lenQuotes == 1:
        index = 0
    else:
        index = randrange (lenQuotes)

    print (str (items[index]['Quote']) + " by " + str (items[index]['Author']))
    return "The quote is: " + str (items[index]['Quote']) + " by " + str (items[index]['Author'])


def lambda_handler(category, author):


    quote = getQuote (category, author)

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": quote
            }
        }
    }
    return response

if (__name__ == "__main__"):

    client = boto3.client('lambda')

    if sys.argv[1] == '0':

        category = "life"
        author = "any"
        path = './testFindQuoteByCategoryAndAuthor.csv'
    else:
        category = "sport"
        author = "any"
        path = './testPublishToTopic.csv'

    for i in range (100):
        start = time.time ()

        #response = lambda_handler (category, author)
        response = client.invoke (
            FunctionName='arn:aws:lambda:us-east-1:638927402797:function:FindQuoteByCategoryAuthor',
            InvocationType='RequestResponse',
            Payload=json.dumps('./input.json')
        )

        end = time.time ()
        elapsed = end - start

        with open (path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])



    #print ('result = ' + str (response))

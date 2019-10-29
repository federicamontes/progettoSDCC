import pymongo as pymongo
from random import randrange
import os
import json
import requests
import csv
import boto3
import time

path = './testFindQuoteByTags.csv'


def slack_callout(quote, startTime):
    try:
        response = {"text": quote,
                    "channel": "#%s" % (os.environ['SLACK_CHANNEL'])}

        end = time.time ()
        elapsed = end - start

        with open (path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])

        slack_response = requests.post(os.environ['SLACK_CHANNEL'], json=response,
                                       headers={'Content-Type': 'application/json'})
        return slack_response.status_code
    except:
        return "errore"


def getQuoteByTags(tag, author):
    # connection to MongoAtlas
    client = pymongo.MongoClient(os.environ["MONGODB_ATLAS_CLUSTER_URI"])
    collection = client.test['quotes']

    if author == "any":
        items = list(collection.find({"Tags": tag}))
    else:
        items = list(collection.find({"Tags": tag, "Author": {'$regex': author, '$options': 'i'}}))

    #print(len(items))

    if len(items) == 0:
        return "No quotes! Why don't you try to insert a new one yourself?"
    else:
        index = randrange(len(items))

    print(str(items[index]['Quote']) + " by " + str(items[index]['Author']))
    return str(items[index]['Quote']) + " by " + str(items[index]['Author'])


def lambda_handler(startTime):

    parsed_message = json.loads('{"Category":"sports", "Author":"any"}')

    tag = parsed_message['Category']
    author = parsed_message['Author']


    """
    --Test confirmed subscription--
    client = boto3.client('sns')
    response = client.get_subscription_attributes(
    SubscriptionArn='arn:aws:sns:us-east-1:638927402797:TagForQuote:10a8fa87-ce8d-4182-b75b-1f2db592b40f')

    print(response)
    """

    quote = getQuoteByTags(tag, author)
    slack_msg = slack_callout(quote, startTime)

    return slack_msg


if __name__ == "__main__":


    for i in range (100):
        start = time.time ()

        response = lambda_handler(start)





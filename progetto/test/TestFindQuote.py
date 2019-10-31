import pymongo as pymongo
from random import randrange
import os
import json
import boto3
import time
import csv
import sys



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

        response = client.invoke (
            FunctionName='LAMBDA_ARN',
            InvocationType='RequestResponse',
            Payload=json.dumps('./input.json')
        )

        end = time.time ()
        elapsed = end - start

        with open (path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])




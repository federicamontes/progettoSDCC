import pymongo as pymongo
from random import randrange
import os
import json
import requests
import csv
import boto3
import time

path = './testFindQuoteByTags.csv'


if __name__ == "__main__":

    client = boto3.client ('lambda')

    for i in range (100):
        
        start = time.time ()

        response = client.invoke (
            FunctionName='LAMBDA_ARN',
            InvocationType='RequestResponse',
            Payload=json.dumps ('{"Category":"sports", "Author":"any"}')
        )

        end = time.time ()
        elapsed = end - start

        with open (path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])




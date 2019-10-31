import json
import boto3
from boto3.dynamodb.conditions import Key, Attr, And
from random import randrange
import time
import csv




if __name__ == "__main__":

    client = boto3.client('lambda')

    path ='./testFindQuoteDynamo.csv'

    for i in range (100):
        start = time.time ()

        response = client.invoke (
            FunctionName='ARN_LAMBDA_DYNAMO',
            InvocationType='RequestResponse',
            Payload=json.dumps('./input.json')
        )

        end = time.time ()
        elapsed = end - start

        with open (path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])
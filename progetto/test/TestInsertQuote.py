import boto3
import sys
import time
import json
import csv


if (__name__ == "__main__"):

    client = boto3.client('lambda')

    path = './testInsertQuote.csv'

    for i in range (100):
        start = time.time ()

        response = client.invoke (
            FunctionName='arn:aws:lambda:us-east-1:638927402797:function:InsertNewQuote',
            InvocationType='Event',
            Payload=json.dumps("Don't cry because it's over, smile because it happened. By Dr. Seuss")
        )

        end = time.time ()
        elapsed = end - start

        with open (path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])

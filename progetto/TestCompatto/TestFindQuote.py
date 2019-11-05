import boto3
import time
import csv
import sys

"""
0: FindQuoteByCategoryAuthor
1: FindQuoteByTags
2: InsertNewQuote
"""

if __name__ == "__main__":

    client = boto3.client('lambda')

    if sys.argv[1] == '0':
        Arn = "FindQuoteByCategoryAuthor"
        category = "life"
        author = "any"
        path = './testFindQuoteByCategoryAndAuthor.csv'
        test = './inputCaAu.json'
    elif sys.argv[1] == '1':
        Arn = "FindQuoteByCategoryAuthor"
        category = "sport"
        author = "any"
        path = './testPublishToTopic.csv'
        test = './inputCaAu.json'
    elif sys.argv[1] == '2':
        Arn = "FindQuoteByTags"
        category = "sport"
        author = "any"
        path = './testFindByTags.csv'
        test = './inputTags.json'
    elif sys.argv[1] == '3':
        Arn = "InsertNewQuote"
        path = './testInsertNewQuote.csv'
        test = './inputInsert.json'
    elif sys.argv[1] == '4':
        Arn = "lambdaDynamo"
        path = './testLambdaDynamo.csv'
        test = './inputCaAu.json'

    for i in range(100):
        start = time.time()

        response = client.invoke(
            FunctionName=Arn,
            InvocationType='RequestResponse',
            Payload=open(test, 'rb')
        )

        end = time.time()
        elapsed = end - start

        with open(path, mode='a') as test_file:
            test_writer = csv.writer (test_file, delimiter=';')
            test_writer.writerow ([elapsed])
    print("end")

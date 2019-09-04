import json
from pprint import pprint

import boto3

dir = "Dynamo/quotes.json" #directory file json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://dynamodb.us-east-1.amazonaws.com')

table = dynamodb.Table('Quotes')


def format_object(line):

    if line["Category"] == "":
        response = table.put_item(
            Item={
                'Author': line["Author"],
                'Category': "other",
                'Popularity': str(line["Popularity"]),
                'Quote': line["Quote"],
                'Tags': line["Tags"]
            }
        )

    else:
        response = table.put_item(
            Item={
                'Author': line["Author"],
                'Category': line["Category"],
                'Popularity': str(line["Popularity"]),
                'Quote': line["Quote"],
                'Tags': line["Tags"]
            }
        )


if (__name__ == "__main__"):


    with open(dir) as json_data:
        file = json.load(json_data)
        json_data.close()
        # pprint(file)


    for line in file:
        # pprint(line["Category"])
        for i in range(0, len(file), 1000):
            print(i)

        format_object(line)

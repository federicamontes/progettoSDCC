import json
import boto3
from boto3.dynamodb.conditions import Key, Attr, And
from random import randrange


# always start with the lambda_handler
def getQuote(author, category):
    # make the connection to dynamodb
    dynamodb = boto3.resource('dynamodb')

    # select the table
    table = dynamodb.Table("Quotes")

    if (author == ""):
        items = table.query(KeyConditionExpression=Key('Category').eq(category))

        lenQuotes = len(items['Items'])
        print(lenQuotes)

        if (lenQuotes == 0):
            return "No quotes!"
        if (lenQuotes == 1):
            index = 0
        else:
            index = randrange(lenQuotes)

        return str(items['Items'][index]['Quote']) + " by " + str(items['Items'][index]['Author'])

    else:

        itemsCat = table.query(KeyConditionExpression=Key('Category').eq(category))

        response = []

        for i in range(len(itemsCat['Items'])):
            if (author in itemsCat['Items'][i]['Author']):
                print(itemsCat['Items'][i]['Quote'])
                response.append(itemsCat['Items'][i])
                print('\n')

        lenQuotes = len(response)
        print(lenQuotes)

        if (lenQuotes == 0):
            return "No quotes!"
        if (lenQuotes == 1):
            index = 0
        else:
            index = randrange(lenQuotes)

        return str(response[index]['Quote']) + " by " + str(response[index]['Author'])


def lambda_handler(event, context):
    print('received request: ' + str(event))
    category = event['currentIntent']['slots']['Category']
    author = event['currentIntent']['slots']['Author']

    if author == 'any':
        author = ""

    if category == 'any':
        category = 'other'

    quote = getQuote(author, category)

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": "The quote is: {Quote}".format(Quote=quote)
            },
        }
    }

    print('result = ' + str(response))
    return response

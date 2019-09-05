import boto3
from boto3.dynamodb.conditions import Key
from random import randrange


def getRandomIndex(len_quotes):
    if len_quotes == 1:
        index = 0
    else:
        index = randrange(len_quotes)
    return index


# always start with the lambda_handler
def getQuote(author, category):
    # make the connection to dynamodb
    dynamodb = boto3.resource('dynamodb')

    # select the table
    table = dynamodb.Table("Quotes")

    items = table.query(KeyConditionExpression=Key('Category').eq(category))
    len_quotes = len(items['Items'])
    print(len_quotes)

    if author == "":
        if len_quotes == 0:
            return "No quotes!"
        else:
            index = getRandomIndex(len_quotes)
            print(items['Items'][index]['Category'])
            return str(items['Items'][index]['Quote']) + " by " + str(items['Items'][index]['Author'])

    else:
        response = []

        for i in range(len(items['Items'])):
            if (author in items['Items'][i]['Author']):
                print(items['Items'][i]['Quote'])
                response.append(items['Items'][i])
                print('\n')

    len_quotes = len(response)
    print(len_quotes)

    if len_quotes == 0:
        return "No quotes!"
    if len_quotes == 1:
        index = 0
    else:
        index = randrange(len_quotes)

    return str(response[index]['Quote']) + " by " + str(response[index]['Author'])


def lambda_handler(event, context):
    category = event['currentIntent']['slots']['Category']
    author = event['currentIntent']['slots']['Author']

    if category == 'any':
        category = 'other'
    #if author == 'null':
    if author is None:
        author = ""

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

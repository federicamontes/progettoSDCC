import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

#always start with the lambda_handler
def getQuote(category):

    # make the connection to dynamodb
    dynamodb = boto3.resource('dynamodb')

    # select the table
    table = dynamodb.Table("Quotes")

    # get item from database
    items = table.get_item(Key={"Category": category})
    
    return items["Item"]["Quote"]
    
    
def lambda_handler(event, context):
    print('received request: ' + str(event))
    #date_input = event['currentIntent']['slots']['Category']
    category = event['currentIntent']['slots']['Category']
    print(category)
    quote = getQuote(category)
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

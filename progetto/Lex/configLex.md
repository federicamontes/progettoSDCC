#CREATE BOT

## 1.customize types model
```
$ aws lex-models put-slot-type --region us-east-1 --name QuotesCategory --cli-input-json file://QuotesCategory.json 
$ aws lex-models put-slot-type --region us-east-1 --name QuotesAuthor --cli-input-json file://QuotesAuthor.json
```

## 2.create lambdaDynamo
nel campo --role è necessario inserire l'arn dell'utente con i permessi lambda/DynamoDB

####create
```
$ aws lambda create-function \
--function-name lambdaDynamo \
--zip-file fileb://get_quote.zip \
--handler get_quote.lambda_handler \
--runtime python3.7 --role arn:aws:iam::268810246503:role/lambda-role \
--timeout 30 --memory-size 256 
```
####update
```
$ aws lambda update-function-code --function-name lambdaDynamo --zip-file fileb://get_quote.zip
```
####delete
```
$ aws lambda delete-function --function-name lambdaDynamo
```

## 3.add lambda func to intent
Inserire l'arn della funzione lambda nel campo "uri" in "fulfillmentActivity"

-create permission
```
aws lambda add-permission \
--region us-east-1 \
--function-name lambdaDynamo \
--statement-id LexGettingStarted-QuotesBotModel \
--action lambda:InvokeFunction --principal lex.amazonaws.com \
--source-arn "arn:aws:lex:us-east-1:268810246503:intent:QuotesIntent:*"
```

## 4.customize intent model

####create
```
$ aws lex-models put-intent \
--region us-east-1 \
--name QuotesIntent \
--cli-input-json file://QuotesIntent.json
```
####delete
```
$ aws lex-models delete-intent --name QuotesIntent
```


## 5.customize bot model

####create
```
$ aws lex-models put-bot --region us-east-1 --name QuotesBotModel --cli-input-json file://QuotesBot.json
```
####delete
```
$ aws lex-models delete-bot --name QuotesBotModel
```
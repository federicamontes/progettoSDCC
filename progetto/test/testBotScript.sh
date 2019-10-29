#! /bin/bash

#se serve lex usare questi parametri
bot_name='QuotesBotModel'
bot_alias='SiPY'
user_id='client'

category='life'
author='any'


for i in $(seq 1 10); do

	post_text()
	{
#------------Comando per collegarsi a Lex
	    #cmd="aws lex-runtime post-text --region us-east-1 --bot-name=$bot_name --bot-alias=$bot_alias --user-id=$user_id"
#-----------Comando per invocare direttamente la lambda
	    cmd="aws lambda invoke --function-name ARN_LAMBDA --invocation-type RequestResponse --payload 'file://input.json' response.json"
#-----------Usare solo se si usa il comando per Lex------------
	    #$cmd --input-text "Give me a quote about $category by $author"
	}
#-------Usare solo se si usa il comando per Lex----------
	#r=$(post_text 'Give me a quote about $category by $author')
	#echo "$r" | ${jq:-cat -}
	echo "sono vivo"
	i=$(( i + 1 ))
done



function getTagsList(arr) {

    return arr.filter(function(ele){
       return ele.length >4;
    });

}

function createJSON (input){
    var result = input.split(" ");
    var quote = result.slice(0, result.indexOf('by'));
    var author = (result.slice(result.indexOf('by')+1)).join(" ");

    return {
        Quote: quote.join(" "),
        Author: author,
        Tags: getTagsList(quote),
        Popularity: Math.random(),
        Category: "other"
    };

}


'use strict';
var MongoClient = require('mongodb').MongoClient;
var hrstart;
var hrend;

const fs = require('fs');


function insert() {
    //exports.handler = (event, context, callback) => {
    //Mongo Atlas URI is setted as lambda's env var
    var uri = process.env['mongodb+srv://adminMongoDB:adminMongoDB@clusterquotes-qnz49.mongodb.net/admin?retryWrites=true&w=majority'];


    //start measuring time
    hrstart = process.hrtime();

    //create connection
    const client = new MongoClient(uri, {useNewUrlParser: true});
    client.connect(err => {
        if (err) throw err;
        //select specific db's collection
        const collection = client.db("test").collection("quotes");

        //processing the input string creating the json
        console.log('connessione al db');
        var quote = 'Stay true to yourself and listen to your inner voice. It will lead you to your dream. by James Ross'
        var newQuoteJSON = createJSON(quote);

        collection.findOne({Quote: newQuoteJSON.Quote}, function (err, result) {
            if (err) throw err;

            if (!result) {
                //insert in db if it does not exist
                collection.insertOne(newQuoteJSON, function (err, res) {
                    if (err) throw err;
                    //end measuring time
                    hrend = process.hrtime(hrstart);
                    fs.appendFile('./testInsertQuote.csv', hrend, function (err) {
                          if (err) throw err;
                          console.log('Saved!');
                        });
                    context.succeed("Your quote has been inserted. Try me c:");

                });
            } else {
                //does not insert in db
                hrend = process.hrtime(hrstart);
                    fs.appendFile('./testInsertQuote.csv', hrend, function (err) {
                          if (err) throw err;
                          console.log('Saved!');
                        });
                context.succeed("Your quote is already here. Find it ;)");
            }

        });

        /*test:
        collection.estimatedDocumentCount({}, function(error, numOfDocs){
                if(error) console.log('errore '+error);
                 context.succeed('Number of quotes updated: '+ numOfDocs);
        });*/

    });


};

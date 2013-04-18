#!/bin/sh
mkdir javabin
javac SentimentTagger.java -cp ark-tweet-nlp-0.3.2.jar -d javabin

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import csv
import codecs
from extractors.statsextractor import DefiniteSentimentExtractor as sent
import hashlib
class GoldTweet(object):

    def __init__(self,tweetID):
        self.tweetID = tweetID
        self.tweet = None

    def __str__(self):
        return "%s: %s" % (self.tweetID, self.tweet)

def _getDaiAnnotation(token):
    #"positive", "negative", "neutral" or "na" (for irrelevant/unclear).    
    if token == "positive":
        return sent.POS
    elif token == "negative":
        return sent.NEG
    elif token == "neutral":    
        return sent.NEU
    elif token == "na":
        return None
    else:
        raise ValueError("Unknown annotation: %s" % token)


def loadDaiTweets(csvFile):
    fh = open(csvFile, "r")
    reader = csv.reader(fh, delimiter='\t'.encode('utf-8'))
    # skip header
    reader.next()
    for row in reader:
        #sentiment numberagreed tweetid tweet
        t = GoldTweet(row[2].decode("utf-8"))
        t.tweet = row[3].decode("utf-8")
        se = row[0].decode("utf-8")
        t.goldStats = { "sentiment" : _getDaiAnnotation(se), "numberagreed" : int(row[1]) }
        yield t
    fh.close() 

def _getCuiAnnotation(token):
    if token == "&":
        # not sure
        return None
    elif token == "+":
        return sent.POS
    elif token == "-":
        return sent.NEG
    elif token == "0":
        return sent.NEU
    else:
        raise ValueError("Unknown annotation: %s" % token)

def loadCuiTweets(csvFile, annotationsFile, lang="de"):
    fh = open(annotationsFile)
    reader = csv.reader(fh, delimiter="\t".encode("utf-8"))
    sentiment = []
    numberagreed = []
    for row in reader:
        if row[0].decode("utf-8").startswith("#"):
            # is comment
            continue
        sentiment.append(_getCuiAnnotation(row[0].decode("utf-8")))
        na = row[1].decode("utf-8")[0]
        numberagreed.append(int(na))
    fh.close()
    fh = open(csvFile)
    reader = csv.reader(fh, delimiter="\t".encode("utf-8"))
    count = 0
    for row in reader:
        # 6       205     en      0.73906744      2009-06-11 Tweet TweetEN
        l = row[2].decode("utf-8").strip()
        if l == lang:
            se = sentiment[count]
            if se is None:
                # "not sure"
                continue
            date = row[4].decode("utf-8")
            tweet = row[5].decode("utf-8")
            t = GoldTweet(hashlib.md5((tweet + date).encode("utf-8")).hexdigest())
            t.tweet = tweet
            t.goldStats = {"sentiment" : sentiment[count],
                "numberagreed": numberagreed[count]}
            yield t
        count += 1
    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: script.py csvFile annotationsFile"
        sys.exit(1)
    csvFile = sys.argv[1]
    annotationsFile = sys.argv[2]
    for tweet in loadCuiTweets(csvFile, annotationsFile):
        print tweet.tweet
        print tweet.goldStats


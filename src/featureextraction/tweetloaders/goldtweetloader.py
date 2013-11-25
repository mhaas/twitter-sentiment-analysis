#-*- coding: utf-8 -*-

"""Loads tweets from Gold standard data sets."""

from __future__ import unicode_literals

import tweetloader
import os
import csv
import codecs
from featureextraction.extractors.statsextractor import DefiniteSentimentExtractor as sent
import hashlib
import socket
import json
from StringIO import StringIO

class GoldTweet(object):
    """Tweet object.
    
    Modelled after Tweet class, but does not load
    data on its own.
    TODO: needs refactoring.
    """

    def __init__(self,tweetID):
        """Constructor.

        Args:
            - tweetID: string, ID of tweet
        """
        self.tweetID = tweetID
        self.tweet = None

    def __str__(self):
        return "%s: %s" % (self.tweetID, self.tweet)

def _getDaiAnnotation(token):
    """Normalizes annotations from DAI data set."""
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
    """Loads tweets from CSV file provided by DAI.
    
    Args:
        - csvFile: string, path to file
    Yields:
        - tweet objects
    """
    fh = open(csvFile, "r")
    reader = csv.reader(fh, delimiter='\t'.encode('utf-8'))
    # skip header
    reader.next()
    for row in reader:
        #sentiment numberagreed tweetid tweet
        t = GoldTweet(row[2].decode("utf-8"))
        t.tweet = row[3].decode("utf-8")
        se = row[0].decode("utf-8")
        getRemoteStats(t)
        sentiment = _getDaiAnnotation(se)
        if not sentiment:
            # can be None
            continue 
        t.goldStats = { "sentiment" : sentiment, "numberagreed" : int(row[1]) }
        yield t
    fh.close() 

def _getCuiAnnotation(token):
    """Normalizes annotations from CUI data set."""
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
    """Loads tweets from CSV files provided by CUI.
    
    Args:
        - csvFile: string, file containing tweets.
        - annotationsFile: string, file containing annotations.
        - lang: which language to load, see file for available options.
    Yields:
        Tweet objects.
    """
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
            getRemoteStats(t)
            t.goldStats = {"sentiment" : sentiment[count],
                "numberagreed": numberagreed[count]}
            yield t
        count += 1

def getRemoteStats(tweetObj):
    """Fetches stats from taggerserver.

    Taggerserver implements the preprocessing.
    tweetObj.tweet is sent to the TaggerServer,
    which returns a tagged version of the tweet
    along with sentiment stats.
    See tweetloader.loadTweetSentiment documentation for available stats.

    Args:
        - tweetObj: Tweet object
    Returns:
        tweetObj with tokens, tags and stats
    """
    remote_host = "localhost";
    remote_port = 1234;

    #create an INET, STREAMing socket
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    #now connect to the web server on port 80
    # - the normal http port
    s.connect((remote_host, remote_port))
    fh = s.makefile()
    assert type(tweetObj.tweet) == unicode
    fh.write(tweetObj.tweet.encode("utf-8"))
    fh.write("\n\n")
    fh.flush()
    l = fh.readline().decode("utf-8")
    stats = json.loads(l)
    tweetObj.stats = stats
    statsFH = StringIO("".join(stats["tweet"]).encode("utf-8"))
    tweetloader.loadTweetSentiment(tweetObj, fh=statsFH)
    del stats["tweet"]
    return tweetObj

    




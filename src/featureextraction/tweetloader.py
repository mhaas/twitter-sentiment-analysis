#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import csv

class Tweet(object):

    def __init__(self, baseDir, tweetID):
        self.baseDir = baseDir
        self.tweetID = tweetID
        self.tweet = None
        self._load()

    def _load(self):
        self._loadTweet()
        self._loadTweetSentiment()
        self._loadTweetStats()
 
    def _loadTweet(self):
        fName = "tweet"
        path = os.path.join(self.baseDir, self.tweetID, fName)
        self.tweet = ""
        fh = open(path, "r")
        for line in fh.readlines():
            self.tweet += line.decode("utf-8")
        fh.close() 

    def _loadTweetSentiment(self):
        fName = "tweet_sentiment"
        path = os.path.join(self.baseDir, self.tweetID, fName)
        # will    W       neutral
        fh = open(path, "r")
        reader = csv.reader(fh, delimiter="\t".encode("ascii"), quoting=csv.QUOTE_NONE)
        self.tokens = []
        self.tokenTypes = []
        self.tokenSentiment = []
        for row in reader:
            self.tokens.append(row[0])
            self.tokenTypes.append(row[1])
            self.tokenSentiment.append(row[2])
        fh.close()

    # {u'pos_smileys': 0.0, u'pos_tokens': 0.0, u'tokens': 22.0, u'overall_sentiment_score': 0.0, u'neutral_tokens': 22.0, u'neg_tokens': 0.0, u'neutral_smileys': 0.0, u'neg_smileys': 0.0, u'normalized_sentiment_score': 0.0}
    def _loadTweetStats(self):
        fName = "tweet_stats"
        path = os.path.join(self.baseDir, self.tweetID, fName)
        fh = open(path, "r")
        reader = csv.reader(fh, delimiter=':'.encode("ascii"), quoting=csv.QUOTE_NONE)
        self.stats = {}
        for row in reader:
            key = row[0].strip().replace(" ", "_")
            self.stats[key] = float(row[1].strip())
        fh.close()

    def __str__(self):
        return "Tweet: %s, %s" % (self.tweetID, self.tweet)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: script.py dataDir tweetID"
        sys.exit(1)
    dataDir = sys.argv[1]
    tweetID = sys.argv[2]
    t = Tweet(dataDir, tweetID)
    print str(t)
    print t.tokens
    print t.tokenTypes
    print t.tokenSentiment
    print t.stats

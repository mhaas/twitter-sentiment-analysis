#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import csv

class Tweet(object):
    """Class representing tweet.
    
    Loads its data from preprocessed tweets.
    """
    
    def __init__(self, baseDir, tweetID):
        """Constructor.

        Args:
            baseDir: directory string containing tweet subdirectories
            tweetID: string ID of tweet
        """
        self.baseDir = baseDir
        self.tweetID = tweetID
        self.tweet = None
        self._load()

    def _load(self):
        """Loads all tweet data from disk"""
        self._loadTweet()
        self._loadTweetSentiment()
        self._loadTweetStats()
 
    def _loadTweet(self):
        """Load full tweet text from disk.

        Full text can be accessed in self.tweet.
        """
        fName = "tweet"
        path = os.path.join(self.baseDir, self.tweetID, fName)
        self.tweet = ""
        fh = open(path, "r")
        for line in fh.readlines():
            self.tweet += line.decode("utf-8")
        fh.close() 

    def _loadTweetSentiment(self):
        """Loads tokenized and annotated version of tweet.
        
        Content available in self.tokens, self.tokenTypes and
        self.tokenSentiment.
        """
        fName = "tweet_sentiment"
        path = os.path.join(self.baseDir, self.tweetID, fName)
        # will    W       neutral
        fh = open(path, "r")
        loadTweetSentiment(self, fh)

    # {u'pos_smileys': 0.0, u'pos_tokens': 0.0, u'tokens': 22.0, u'overall_sentiment_score': 0.0, u'neutral_tokens': 22.0, u'neg_tokens': 0.0, u'neutral_smileys': 0.0, u'neg_smileys': 0.0, u'normalized_sentiment_score': 0.0}
    def _loadTweetStats(self):
        """Loads tweet stats from preprocessed data.

        Content available in self.stats dictionary with the following fields:
            - pos_smileys
            - pos_tokens
            - tokens
            - overall_sentiment_score
            - neutral_tokens
            - neg_tokens
            - neutral_smileys
            - neg_smileys
            - normalized_sentiment_score
        """
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

def loadTweetSentiment(tweet, fh):
    """Loads tweet sentiment from tab-separated values file.
    
    First column is token, second column is type, third column is
    sentiment.

    Content is stored in tweet object in tweet.tokens,
    tweet.tokenTypes and tweet.tokenSentiment.
    Args:
        - tweet: Tweet object.
        - fh: file handle.
    Returns:
        Modified tweet object.
    """
    reader = csv.reader(fh, delimiter="\t".encode("ascii"), quoting=csv.QUOTE_NONE)
    tweet.tokens = []
    tweet.tokenTypes = []
    tweet.tokenSentiment = []
    for row in reader:
        tweet.tokens.append(row[0])
        tweet.tokenTypes.append(row[1])
        tweet.tokenSentiment.append(row[2])
    fh.close()
    return tweet


def loadTweets(baseDir):
    """Loads tweets from baseDir.
    Args:
        baseDir: string, directory where tweet directories are located
    Yields:
        Tweet instances.
    """
    for (dirpath, dirnames, filenames) in os.walk(baseDir):
        for directory in dirnames:
            # single-character top level dir?
            if len(directory) == 1:
                continue
            t = Tweet(dirpath, directory)
            yield t

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

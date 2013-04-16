#-*- coding: utf-8 -*-

from __future__ import unicode_literals

class BaseExtractor(object):

    def __init__(self):
        raise NotImplementedError

  # always returns collections.OrderedDict
    def extractFeatures(self, tweet):
        raise NotImplementedError

    def getFields(self):
        raise NotImplementedError
   
    # ARFF datatype declaration
    def getFieldType(self, field):
        return "real"


class TweetIDExtractor(BaseExtractor):
    def __init__(self):
        pass

    def extractFeatures(self, tweet):
        return tweet.tweetID

    def getFields(self):
        return ["tweetID"]

    


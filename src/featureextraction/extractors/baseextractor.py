#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import OrderedDict


class BaseExtractor(object):
    """Base class for all extractors.

    Extractors must override
    * __init__
    * extractFeatures
    * getFields
    Extractors may override getFieldType
    if the ARFF field data type is not "real".
    """
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
    """Extracts Tweet ID."""
    def __init__(self):
        pass

    def extractFeatures(self, tweet):
        ret = OrderedDict()
        ret["tweetID"] = tweet.tweetID
        return ret

    def getFields(self):
        return ["tweetID"]

    # TODO - can weka handle big numbers?
    def getFieldType(self, field):
        return "string"

    


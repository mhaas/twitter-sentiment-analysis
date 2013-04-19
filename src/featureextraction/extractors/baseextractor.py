#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import OrderedDict

"""Basic feature extractors.""" 

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
        """Extracts Features from tweet.

        Must return OrderedDict object.
        Args:
            - tweet: Tweet object
        Returns:
            - OrderedDict
        """
        raise NotImplementedError

    def getFields(self):
        """Returns field names for this extractor.

        This methods returns the attribute names for
        the features extracted in this class.
        
        Returns:
            list of attribute name strings
        """
        raise NotImplementedError
   
    # ARFF datatype declaration
    def getFieldType(self, field):
        """Returns data type for given field

        Fields can have different fields and need
        to be declared accordingly. Valid field types
        can be found in the ARFF spec.

        Returns:
            field type as string
        Raises:
            ValueError: if unknown field is passed in
        """
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

    def getFieldType(self, field):
        return "string"

    


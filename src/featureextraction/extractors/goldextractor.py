#-*- coding: utf-8 -*-

"""Extracts Gold Standard sentiment."""

from __future__ import unicode_literals
from collections import OrderedDict
from baseextractor import BaseExtractor


class GoldExtractor(BaseExtractor):
    """Extracts Gold Standard sentiment.
    
    Fields/types:
        - gold_sentiment/nominal: sentiment for tweet. {pos, neg, neut}
        - gold_sentiment_agreement/numeric: annotator agreement
    """
    def __init__(self):
        pass

    def extractFeatures(self, tweet):
        ret = OrderedDict()
        ret["gold_sentiment"] = tweet.goldStats["sentiment"]
        ret["gold_sentiment_agreement"] = tweet.goldStats["numberagreed"]
        return ret

    def getFields(self):
        return ["gold_sentiment", "gold_sentiment_agreement"]

    POS = "pos"
    NEG = "neg"
    NEU = "neut"
    F_SMI = "def_sentiment_smiley"
    F_A = "def_sentiment_analysis"

    # ARFF nominal attribute syntax
    def getFieldType(self, field):
        if field == "gold_sentiment":
            return "{%s,%s,%s}" % (self.POS, self.NEG, self.NEU)
        elif field == "gold_sentiment_agreement":
            return "numeric"
        else:
            raise ValueError("Unknown field %s" % field)



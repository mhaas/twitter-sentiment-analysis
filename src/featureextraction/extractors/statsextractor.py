# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from baseextractor import BaseExtractor
from collections import OrderedDict
#{u'pos_smileys': 0.0, u'pos_tokens': 0.0, u'tokens': 22.0, u'overall_sentiment_score': 0.0, u'neutral_tokens': 22.0, u'neg_tokens': 0.0, u'neutral_smileys': 0.0, u'neg_smileys': 0.0, u'normalized_sentiment_score': 0.0}

class BaseStatsExtractor(BaseExtractor):

    def extractFeatures(self, tweet):
        res = OrderedDict()
        for f in self.fields:
            res[f] = tweet.stats[f]
        return res

    def getFields(self):
        return self.fields


class TokenCountExtractor(BaseStatsExtractor):

    def __init__(self):
        self.fields = ["tokens"]

class NormalizedSentimentScoreExtractor(BaseStatsExtractor):

    def __init__(self):
        self.fields = ["normalized_sentiment_score"]


class SmileyCountExtractor(BaseStatsExtractor):
    def __init__(self):
        self.fields = ["neutral_smileys", "neg_smileys", "pos_smileys"]


class DefiniteSentimentExtractor(BaseExtractor):
    """Gives Sentiment as "pos", "neg" or "neut".

        Unlike other extractors, this extractor does not return a numeric value.
        It returns a definite value from set {"pos", "neg", "neut"}.
    """
    POS = "pos"
    NEG = "neg"
    NEU = "neut"
    F_SMI = "def_sentiment_smiley"
    F_A = "def_sentiment_analysis"

    def __init__(self):
        pass

    def extractFeatures(self, tweet):
        ret = OrderedDict()
        if tweet.stats["pos_smileys"] > 0 and tweet.stats["neg_smileys"] > 0:
            ret[self.F_SMI] = self.NEU
        elif tweet.stats["pos_smileys"] > 0:
            ret[self.F_SMI] = self.POS
        elif tweet.stats["neg_smileys"] > 0:
            ret[self.F_SMI] = self.NEG
        else:
            ret[self.F_SMI] = self.NEU
        # ignore neutral smileys for now
        
        # use results from sentiment analysis
        if tweet.stats["normalized_sentiment_score"] < 0:
            ret[self.F_A] = self.NEG
        elif tweet.stats["normalized_sentiment_score"] > 0:
            ret[self.F_A] = self.POS
        else:
            ret[self.F_A] = self.NEU 
        return ret

    def getFields(self):
        return [self.F_SMI, self.F_A]

    # ARFF nominal attribute syntax
    def getFieldType(self, field):
        return "{%s,%s,%s}" % (self.POS, self.NEG, self.NEU)



# -*- coding: utf-8 -*-

"""Extractors for feature originating from sentiment stats.

    Sentiment stats come from the preprocessing module,
    see taggerserver and tweetloaders.
"""

from __future__ import unicode_literals

from baseextractor import BaseExtractor
from collections import OrderedDict


class BaseStatsExtractor(BaseExtractor):
    """Base class for stats extractors.

    All stats extractors use the tweet.stats member.
    Child classes declare which fields they extract
    from tweet.stats and this class handles the
    extraction.
    
    Child classes must set self.fields to a list of
    fields to be extracted from tweet.stats.
    """
    def extractFeatures(self, tweet):
        res = OrderedDict()
        for f in self.fields:
            res[f] = tweet.stats[f]
        return res

    def getFields(self):
        return self.fields


class TokenCountExtractor(BaseStatsExtractor):
    """Extracts token count.
    
    Fields/types:
        - tokens/numeric
    """
    def __init__(self):
        self.fields = ["tokens"]

class NormalizedSentimentScoreExtractor(BaseStatsExtractor):
    """Extracts normalized sentiment score.
    
    Fields/types:
        - normalized_sentiment_score/numeric
    """
    def __init__(self):
        self.fields = ["normalized_sentiment_score"]


class SmileyCountExtractor(BaseStatsExtractor):
    """Extracts emoticon counts.

    Fields/types:
        - neutral_smileys/numeric
        - neg_smileys/numeric
        - pos_smileys/numeric
    """
    def __init__(self):
        self.fields = ["neutral_smileys", "neg_smileys", "pos_smileys"]


class DefiniteSentimentExtractor(BaseExtractor):
    """Gives Sentiment as "pos", "neg" or "neut".

        Two sentiment values are returned, one based on emoticons
        and one based on lexicon-backed sentiment analysis done
        by preprocessing.

        Unlike other extractors,
        this extractor does not return a numeric value.
    
        Fields/types:
            - def_sentiment_smiley/nominal {pos, neg, neut}
            - def_sentiment_analysis/nominal {pos, neg, neut}
    """
    POS = "pos"
    NEG = "neg"
    NEU = "neut"
    F_SMI = "def_sentiment_smiley"
    F_A = "def_sentiment_analysis"

    def __init__(self, forceValueSmiley=None, forceValueAnalysis=None): 
        self.forceValueSmiley = forceValueSmiley
        self.forceValueAnalysis = forceValueAnalysis


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
        if self.forceValueSmiley:
            ret[self.F_SMI] = self.forceValueSmiley

 
        # use results from sentiment analysis
        if tweet.stats["normalized_sentiment_score"] < 0:
            ret[self.F_A] = self.NEG
        elif tweet.stats["normalized_sentiment_score"] > 0:
            ret[self.F_A] = self.POS
        else:
            ret[self.F_A] = self.NEU
        if self.forceValueAnalysis:
            ret[self.F_A] = self.forceValueAnalysis 
        return ret

    def getFields(self):
        return [self.F_SMI, self.F_A]

    # ARFF nominal attribute syntax
    def getFieldType(self, field):
        return "{%s,%s,%s}" % (self.POS, self.NEG, self.NEU)



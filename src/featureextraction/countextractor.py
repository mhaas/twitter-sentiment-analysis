# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from baseextractor import BaseExtractor
from collections import OrderedDict
#{u'pos_smileys': 0.0, u'pos_tokens': 0.0, u'tokens': 22.0, u'overall_sentiment_score': 0.0, u'neutral_tokens': 22.0, u'neg_tokens': 0.0, u'neutral_smileys': 0.0, u'neg_smileys': 0.0, u'normalized_sentiment_score': 0.0}


class CountExtractor(BaseExtractor):


    def __init__(self):
        pass

    def extractFeatures(self, tweet):
        res = OrderedDict()
        res["tokens"] = tweet.stats["tokens"]
        return res        


    def getFields(self):
        return ["tokens"]

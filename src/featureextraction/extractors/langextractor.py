# -*- coding: utf-8 -*-

"""Extracts language from tweet."""

from __future__ import unicode_literals

from baseextractor import BaseExtractor
from collections import OrderedDict
#{u'pos_smileys': 0.0, u'pos_tokens': 0.0, u'tokens': 22.0, u'overall_sentiment_score': 0.0, u'neutral_tokens': 22.0, u'neg_tokens': 0.0, u'neutral_smileys': 0.0, u'neg_smileys': 0.0, u'normalized_sentiment_score': 0.0}
import ldig.server


class LDIGLangExtractor(BaseExtractor):
    """Uses LDIG language classifier to determine language for tweet.
    
    Download LDIG here: https://github.com/shuyo/ldig

    Fields/Types:
        - lang_ldig/nominal: {de,..} - depends on LDIG model
    """
    
    def __init__(self, model):
        """Constructor:
        
            Args:
                model: string, LDIG model directory
        """ 
        self.d = ldig.server.Detector(model)
        self.field = "lang_ldig"

    def extractFeatures(self, tweet):
        ret = OrderedDict()
        stats = self.d.detect(tweet.tweet)
        # get best match
        assert len(stats["labels"]) == len(stats["prob"])
        bestMatch = None
        bestMatchProp = -1
        for index in xrange(len(stats["labels"])):
            cur = stats["prob"][index]
            if cur > bestMatchProp:
                bestMatchProp = cur
                bestMatch = stats["labels"][index]
        ret[self.field] = bestMatch
        return ret 

    def getFields(self):
        return [self.field]
    
    def getFieldType(self, field):
        return "{" + ",".join(self.d.labels) + "}"
        


if __name__ == "__main__":
    import sys
    from tweetloaders.goldtweetloader import GoldTweet
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: script.py modelDir"
        print >> sys.stderr, "Provide LDIG model directory as first argument."
        sys.exit(1)
    d = LDIGLangExtractor(sys.argv[1])
    t = GoldTweet("fakeID")
    t.tweet = "Dies ist ein deutscher Tweet"
    print d.extractFeatures(t)
    print d.getFieldType("blah")

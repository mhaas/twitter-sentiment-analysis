# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from baseextractor import BaseExtractor
from collections import OrderedDict
from copy import copy
import codecs
import logging
import re

class TokenVectorExtractor(BaseExtractor):
    def __init__(self):
        raise NotImplementedException

    def _loadFrequentWords(self,f,skipRE=None):
        self.protoDict = OrderedDict()
        fh = codecs.open(f, "r", "utf-8")
        for line in fh:
            cleaned = line.strip()
            if cleaned == "":
                continue
            # ARFF attribute names are case insensitive...
            cleaned = cleaned.lower()
            if skipRE:
                if skipRE.match(cleaned):
                    continue
            self.protoDict[cleaned] = 0
        self.words = frozenset(self.protoDict.keys())
        assert len(self.words) == len(self.protoDict.keys())
        logging.debug("Got this many keys: %s" % len(self.protoDict.keys()))

    def extractFeatures(self, tweet):
        ret = OrderedDict()
        ret.update(self.protoDict)
        for token in tweet.tokens:
            if token in self.words:
                ret[token] += 1
        return ret

    def getFields(self):
        return self.protoDict.keys()


# find . -name tweet -exec cat {} \; | tr ' ' '\n' | sort | uniq -c | sort -rn | head -n 1000 > hitlist.txt
# awk -F" " '{ print $2 }' < hitlist-sorted.txt
class WordVectorExtractor(TokenVectorExtractor):
    
    def __init__(self):
        # skip hashtags to prevent duplicates with HashtagVectorExtractor
        self._loadFrequentWords("../../data/featureextraction/top-words.txt", re.compile(ur"^#.*$"))

# grep '^#' hitlist.txt | head -n 100 > top-tags.txt
class HashtagVectorExtractor(TokenVectorExtractor):

    def __init__(self):
        self._loadFrequentWords("../../data/featureextraction/top-tags.txt")


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from baseextractor import BaseExtractor
from collections import OrderedDict
from copy import copy
import codecs

# find . -name tweet -exec cat {} \; | tr ' ' '\n' | sort | uniq -c | sort -rn | head -n 1000 > hitlist.txt
# awk -F" " '{ print $2 }' < hitlist-sorted.txt
class WordVectorExtractor(BaseExtractor):
    
    def __init__(self):
        self._loadFrequentWords()

    def _loadFrequentWords(self):
        self.protoDict = OrderedDict()
        f = "hitlist.txt"
        fh = codecs.open("hitlist.txt", "r", "utf-8")
        for line in fh:
            self.protoDict[line.strip()] = 0
        self.words = frozenset(self.protoDict.keys())

    def extractFeatures(self, tweet):
        ret = copy(self.protoDict)
        for token in tweet.tokens:
            if token in self.words:
                ret[token] += 1
        return ret

    def getFields(self):
        return self.protoDict.keys()
            
        
    


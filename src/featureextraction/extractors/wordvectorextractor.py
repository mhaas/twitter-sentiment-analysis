# -*- coding: utf-8 -*-

"""Extracts token vector features from tweets"""

from __future__ import unicode_literals
from baseextractor import BaseExtractor
from collections import OrderedDict
from copy import copy
import codecs
import logging
import re

class TokenVectorExtractor(BaseExtractor):
    """Base class for token vector extraction.

    Subclasses provide a list of tokens. If a token
    from this list exists in a tweet, the token count
    is updated.
    The token vector is then the list of counts,
    with each entry reflecting a particular token
    from the supplied list of tokens.
    """
    def __init__(self):
        raise NotImplementedException

    def _loadFrequentWords(self,f,skipRE=None):
        """Loads token list from disk.

        Tokens matching the skipRE argument
        will be skipped
        Args:
            - f: string, file name
            - skipRE: regex object, matched using re.match
        """
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
    """Extracts vector for (most common) words.

    Words are loaded from ../../data/featureextraction/top-words.txt.
    Words starting with '#' are skipped as hashtags are handled in a different class.
    The word list is generated externally and typically contains the top 1000
    common words, sorted by frequency.

    For fields, see word list file.

    Fields/types:
        - <word list>/numeric
    """

    def __init__(self):
        # skip hashtags to prevent duplicates with HashtagVectorExtractor
        self._loadFrequentWords("../../data/featureextraction/hitlist-fixed.txt", re.compile(ur"^#.*$"))


# grep '^#' hitlist.txt | head -n 100 > top-tags.txt
class HashtagVectorExtractor(TokenVectorExtractor):
    """Extracts vector for (most common) hash tags.

    Hash tags are loaded from ../../data/featureextraction/top-tags.txt.
    The hash tag list is generated externally and typically contains the top 100
    common hash tags, sorted by frequency.
    
    For fields, see hash tag list file.

    Fields/types:
        - <hash tag list>/numeric
    """
    def __init__(self):
        self._loadFrequentWords("../../data/featureextraction/hitlist-hashtag-fixed.txt")


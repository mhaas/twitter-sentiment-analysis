# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from baseextractor import BaseExtractor
import re
from collections import OrderedDict


class BasePatternExtractor(BaseExtractor):

    YES = "Y"
    NO = "N"

    def extractFeatures(self, tweet):
        ret = OrderedDict()
        for (field,regex) in self.regexes.iteritems():
            if regex.search(tweet.tweet):
                ret[field] = self.YES
            else:
                ret[field] = self.NO
        return ret
                

    def getFields(self):
        return self.regexes.keys()

    def getFieldType(self, field):
        return "{%s,%s}" % (self.YES,self.NO)


class RepeatedCharacterExtractor(BasePatternExtractor):

    def __init__(self):
        self.regexes = OrderedDict()
        # http://stackoverflow.com/questions/2039140/python-re-how-do-i-match-an-alpha-character
        # regex is not optimal, ignores bmp and has digits and underscore
        self.regexes["min_3_repeated_character"] = re.compile(ur"[^\W\d_]{3}")

class CapsExtractor(BasePatternExtractor):
     def __init__(self):
        self.regexes = OrderedDict()
        # regex is not optimal, ignores bmp
        self.regexes["caps_lock_min_3_characters"] = re.compile(ur"[A-Z]{3}")



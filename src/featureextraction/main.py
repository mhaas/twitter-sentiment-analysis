#/usr/bin/python
# -*- coding: utf-8 -*-

"""Main entry point for feature extraction.

Given directory with preprocessed tweets, extracts features from tweets
and saves as CSV and ARFF files.
"""

from __future__ import unicode_literals

from extractors.baseextractor import TweetIDExtractor
from extractors.statsextractor import TokenCountExtractor,NormalizedSentimentScoreExtractor,SmileyCountExtractor,DefiniteSentimentExtractor
from extractors.wordvectorextractor import WordVectorExtractor,HashtagVectorExtractor
from extractors.textpatternextractor import RepeatedCharacterExtractor,CapsExtractor
from extractors.langextractor import LDIGLangExtractor
from tweetloaders import tweetloader
from collections import OrderedDict
import os
import csv
import codecs
import logging
from datetime import datetime
import sys

logging.basicConfig(filename="main.log", level=logging.DEBUG)

ldig_model = "../../3rdparty/ldig/models/model.latin/"

# configure extractors
# order is important for WEKA/ARFF
extractors = []
extractors.append(TweetIDExtractor())
extractors.append(LDIGLangExtractor(ldig_model))
extractors.append(TokenCountExtractor())
extractors.append(NormalizedSentimentScoreExtractor())
extractors.append(SmileyCountExtractor())
extractors.append(DefiniteSentimentExtractor())
extractors.append(RepeatedCharacterExtractor())
extractors.append(CapsExtractor())
extractors.append(WordVectorExtractor())
extractors.append(HashtagVectorExtractor())


def cleanForARFF(token):
    """Cleans attribute names for use with WEKA.

    Some characters such as single quotes need to be
    replaced or escaped to prevent errors when
    loading the file into WEKA.
    
    Args:
        token: attribute name string to be cleaned

    Returns: clean attribute name string
    """
    token = token.strip()
    if token == "":
        return "--EMPTYSTRING--"
    token = token.replace("'",ur"--SINGLEQUOTE--")
    token = token.replace("%",ur"\%")
    token = token.replace(",","--COMMA--")
    token = token.replace('"', "--DOUBLEQUOTE--")
    return token

def run(tweetIterable, outFile, extractors, writeCSV=False, close=True):
    """Extracts features from tweets.

    Args:
        - tweetIterable: iterable containing Tweet objects
        - outFile: where CSV and ARFF data is stored,
            ARFF is stored with suffix ".arff"
        - extractors: list of extractor objects
    """
    fields = []
    if hasattr(outFile, "write"):
        arffFH = outFile
    else:
        arffFH = codecs.open(outFile + ".arff", "w", "utf-8")
    arffFH.write("@relation twitter-%s\n" % datetime.now().isoformat())
    for e in extractors:
        curFields = e.getFields()
        fields.extend(curFields)
        for f in curFields:
            if not type(f) == unicode:
                print >> sys.stderr, "field is not unicode, %s" % f
                print >> sys.stderr, "make sure your getFields method returns unicode"
                assert type(f) == unicode
            cleaned = cleanForARFF(f)
            if cleaned is None:
                continue
            arffFH.write("@attribute ")
            arffFH.write(cleaned)
            arffFH.write(" %s\n" % e.getFieldType(f))
    arffFH.write("@data\n")

    if writeCSV:
        outFH = codecs.open(outFile, "w", "utf-8")
        o = csv.DictWriter(outFH, fields, extrasaction="ignore")
        # write header manually because unicode brokenness
        #o.writeheader()
        for f in fields:
            outFH.write(f)
            outFH.write(",")
        outFH.write("\n")

    for t in tweetIterable:
        logging.debug("Processing tweet %s", t.tweetID)
        featureVector = OrderedDict()
        for e in extractors:
            featureVector.update(e.extractFeatures(t))
        if writeCSV:
            o.writerow(featureVector)
        noComma = True
        for item in featureVector.values():
            if noComma:
                noComma = False
            else:
                arffFH.write(",")
            arffFH.write(str(item))
        arffFH.write("\n")
    if writeCSV and close:
        outFH.close()
    if close:
        arffFH.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: script.py baseDir outFile"
        sys.exit(1)
    iterable = tweetloader.loadTweets(sys.argv[1])
    run(iterable, sys.argv[2], extractors)
        




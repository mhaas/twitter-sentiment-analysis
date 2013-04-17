#/usr/bin/python
# -*- coding: utf-8 -*-

from extractors.baseextractor import TweetIDExtractor
from extractors.statsextractor import TokenCountExtractor,NormalizedSentimentScoreExtractor,SmileyCountExtractor,DefiniteSentimentExtractor
from extractors.wordvectorextractor import WordVectorExtractor,HashtagVectorExtractor
from extractors.textpatternextractor import RepeatedCharacterExtractor,CapsExtractor
import tweetloader
from collections import OrderedDict
import os
import csv
import codecs
import logging
from datetime import datetime
import sys

logging.basicConfig(filename="main.log", level=logging.DEBUG)

# configure extractors
# order is important for WEKA/ARFF
extractors = []
extractors.append(TweetIDExtractor())
extractors.append(TokenCountExtractor())
extractors.append(NormalizedSentimentScoreExtractor())
extractors.append(SmileyCountExtractor())
extractors.append(DefiniteSentimentExtractor())
extractors.append(RepeatedCharacterExtractor())
extractors.append(CapsExtractor())
extractors.append(WordVectorExtractor())
extractors.append(HashtagVectorExtractor())


def cleanForARFF(token):
    token = token.strip()
    if token == "":
        return "--EMPTYSTRING--"
    token = token.replace("'",ur"--SINGLEQUOTE--")
    token = token.replace("%",ur"\%")
    token = token.replace(",","--COMMA--")
    token = token.replace('"', "--DOUBLEQUOTE--")
    return token

def run(tweetIterable, outFile, extractors):
    fields = []
    arffFH = codecs.open(outFile + ".arff", "w", "utf-8")
    arffFH.write("@relation twitter-%s\n" % datetime.now().isoformat())
    for e in extractors:
        fields.extend(e.getFields())
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

    outFH = codecs.open(outFile, "w", "utf-8")
    o = csv.DictWriter(outFH, fields, extrasaction="ignore")
    # write header manually because unicode brokenness
    #o.writeheader()
    for f in fields:
        outFH.write(f)
        outFH.write(",")
    outFH.write("\n")

    for t in tweetIterable:
        featureVector = OrderedDict()
        for e in extractors:
            featureVector.update(e.extractFeatures(t))
            o.writerow(featureVector)
        noComma = True
        for item in featureVector.values():
            if noComma:
                noComma = False
            else:
                arffFH.write(",")
            arffFH.write(str(item))
        arffFH.write("\n")
    outFH.close()
    arffFH.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: script.py baseDir outFile"
        sys.exit(1)
    iterable = tweetloader.loadTweets(sys.argv[1])
    run(iterable, sys.argv[2], extractors)
        




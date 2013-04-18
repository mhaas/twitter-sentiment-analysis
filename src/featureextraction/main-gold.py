#/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(filename="gold-main.log", level=logging.DEBUG)

import sys
from tweetloaders import goldtweetloader
from extractors.baseextractor import TweetIDExtractor
#from extractors.statsextractor import TokenCountExtractor,NormalizedSentimentScoreExtractor,SmileyCountExtractor,DefiniteSentimentExtractor
#from extractors.wordvectorextractor import WordVectorExtractor,HashtagVectorExtractor
from extractors.textpatternextractor import RepeatedCharacterExtractor,CapsExtractor

from main import cleanForARFF,run
import main

# configure extractors
# order is important for WEKA/ARFF
extractors = []
# basextractor
extractors.append(TweetIDExtractor())
# statsextractor
#extractors.append(TokenCountExtractor())
#extractors.append(NormalizedSentimentScoreExtractor())
#extractors.append(SmileyCountExtractor())
#extractors.append(DefiniteSentimentExtractor())
# textpatternextractor
extractors.append(RepeatedCharacterExtractor())
extractors.append(CapsExtractor())
# wordvectorextractor - need tokens
#extractors.append(WordVectorExtractor())
#extractors.append(HashtagVectorExtractor())

def printUsage():
    print >> sys.stderr, "Usage: script.py [cui|narr] tweetsFile {annotationsfile}"    


if __name__ == "__main__":
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)
    typ = sys.argv[1]
    if typ == "cui":
        if len(sys.argv) < 4:
            printUsage()
            print >> sys.stderr, "Please provide tweets file and annotation file!"
            sys.exit(1)
        loader = goldtweetloader.loadCuiTweets(sys.argv[2], sys.argv[3])
    elif typ == "narr":
        loader = goldtweetloader.loadDaiTweets(sys.argv[2])
    else:
        printUsage
        sys.exit(1)
    run(loader, "out-%s.csv" % typ, main.extractors)
        




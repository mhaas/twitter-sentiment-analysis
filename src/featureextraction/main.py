#/usr/bin/python
# -*- coding: utf-8 -*-

from countextractor import CountExtractor
from wordvectorextractor import WordVectorExtractor
from tweetloader import Tweet
from collections import OrderedDict
import os
import csv
import codecs
import logging

logging.basicConfig(filename="main.log", level=logging.DEBUG)

# configure extractors
# order is important for WEKA/ARFF
extractors = []
extractors.append(CountExtractor())
extractors.append(WordVectorExtractor())


def run(baseDir, outFile):
    fields = []
    for e in extractors:
        fields.extend(e.getFields())
    outFH = codecs.open(outFile, "w", "utf-8")
    o = csv.DictWriter(outFH, fields, extrasaction="ignore")
    for (dirpath, dirnames, filenames) in os.walk(baseDir):
        for directory in dirnames:
            logging.info("Now processing dir %s", os.path.join(dirpath,directory))
            t = Tweet(baseDir, directory)
            featureVector = OrderedDict()
            for e in extractors:
                featureVector.update(e.extractFeatures(t))
            o.writerow(featureVector)
    outFH.close() 

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: script.py baseDir"
        sys.exit(1)
    run(sys.argv[1], "out.csv")
        




import cherrypy
import json

import featureextraction
import featureextraction.tweetloaders.goldtweetloader
import featureextraction.main
from StringIO import StringIO
import urllib2
import logging


def getARFF(tweetObj):
    iterable = [tweetObj]
    fh = StringIO()
    featureextraction.main.run(iterable, fh, featureextraction.main.extractors, close=False)
    logging.debug("Got ARFF for tweet %s: %s", tweetObj, fh.getvalue())
    return fh.getvalue()
    

def getClass(ident, tweet):
    url = "http://localhost:8090/"
    data = json.dumps({ident : tweet})
    logging.debug("Sending request to classifier server %s: %s", url, data)
    req = urllib2.Request(url=url,
                       data=data)
    f = urllib2.urlopen(req)
    ret = json.loads(f.read())
    logging.debug("Response from classifier server: %s", ret)
    if ident in ret:
        return ret[ident]
    else:
        return "unknown"
    

class HelloWorld:
    def index(self, tweets=None, password=None):
        if not password and password != "cheezburger":
            return json.dumps({"error": "Authentication failed"})
        if not tweets:
            return json.dumps({"error": "Must provided tweets parameter"})
        ts = json.loads(tweets)
        res = {}
        for t in ts:
            tweetObj = featureextraction.tweetloaders.goldtweetloader.GoldTweet(t)
            tweetObj.tweet = ts[t]
            featureextraction.tweetloaders.goldtweetloader.getRemoteStats(tweetObj)
            arff = getARFF(tweetObj)
            clazz = getClass(t, arff)
            res[t] = clazz
            logging.info("Class for tweet %s: %s", t, clazz)
        return json.dumps(res)
    index.exposed = True


if __name__ == "__main__":
    cherrypy.quickstart(HelloWorld())


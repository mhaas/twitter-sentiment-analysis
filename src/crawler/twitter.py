#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module dumps tweets originating from Germany to disk as CSV files.

Tweets are obtained from the Twitter Streaming API via the "sample"
endpoint with a "locations" filter set to a bounding box roughly
covering Germany.

Tweets are saved to disk as CSV files.

API credentials are imported from credentials.py which needs
to provide the following fields:
    - consumer_key
    - consumer_secret
    - access_key
    - access_key
"""

import tweepy
import sys
import csv
import datetime
import json

from credentials import consumer_key,consumer_secret,access_key,access_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    """CustomStreamListener dumps received tweets to disk as CSV files."""

    def __init__(self, outFile, api):
        self.api = api
        self.encoding = "utf-8"
        self.fields = [ "user", "created_at", "source", "retweeted_status",
                        "id_str",
                        "in_reply_to_screen_name", "lang", "retweet_count",
                        "text" ]
        #self.fields.append("place") # place is complex object, not that easy to serialize
        self.fields.append("coordinates")
        self.fields.append("entities")
        self.count = 0
        self.writer = csv.DictWriter(open(outFile,"w"), fieldnames = self.fields)
        self.writer.writeheader()

    def on_status(self, status):
        result = {}
        for field in self.fields:
          if hasattr(status, field) and not getattr(status, field) == None:
            if field == "user":
              val = getattr(getattr(status, field), "id_str")
            elif field == "created_at":
              val = getattr(status, field).isoformat()
            elif field == "retweet_count":
              val = str(getattr(status, field))
            elif field == "entities" or field == "coordinates" or field == "place":
              val = json.dumps(getattr(status, field))
            else:
              val = getattr(status, field)
            result[field] = val.encode(self.encoding)
          else:
            result[field] = "".encode(self.encoding)
        self.writer.writerow(result)
        self.count += 1
        if self.count % 1000 == 0:
          print >> sys.stderr, 'Now have received ', self.count, ' tweets'
      

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

cur = datetime.datetime.now().isoformat()
sl = CustomStreamListener("tweets-%s.csv" % cur, api)
sapi = tweepy.streaming.Stream(auth, sl)

# http://www.findlatitudeandlongitude.com/
# Approximately DE
# twitter streaming API has language filter, but not yet operational as of 2013-03-19.
# word on the street is that the language detector is somewhat broken
sapi.filter(locations=[7.4, 48, 12.5, 54.9])


# get random sample from all tweets. 
sapi.sample()

sl.close()


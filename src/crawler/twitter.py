#!/usr/bin/env python
# -*- coding: utf-8 -*-
# We need /usr/bin/env to make virtualenv work.
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


    def __init__(self, outFile, api):
        self.api = api
        # BEI DER MACHT VON GRAYSKULL
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

# Ungefaehr DE - Format der Koordination entspricht nicht OSM BB?
"""
The first two sets of numbers(-80.419922,32.528289) specify the Southwestern corner of one's "bounding box," in longitude/latitude, which is the location one is trying to grab tweets from within. 
"""
# http://www.findlatitudeandlongitude.com/
# ungefaehr DE
sapi.filter(locations=[7.4, 48, 12.5, 54.9])


# get random sample from all tweets. 
sapi.sample()

sl.close()

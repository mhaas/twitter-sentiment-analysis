#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import json
import urllib
import urllib2


def test(tweet):

    url = "http://localhost:8080/"
    data = json.dumps({"54321" : tweet})
    encoded = urllib.urlencode({"tweets" : data, "password": "cheezburger"})
    req = urllib2.Request(url=url,
                       data=encoded)
    f = urllib2.urlopen(req)
    ret = json.loads(f.read())
    print ret
    if "54321" in ret:
        return ret["54321"]
    else:
        return None

if __name__ == "__main__":
    r = test("lol rotflmao <3 :) :) :) ;)")
    print r
    r = test("Ich liebe Katzen und den Tatort xD!!1elf")
    print r


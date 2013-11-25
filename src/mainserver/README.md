Main Server - everything starts here
====================================

The main server is the main entry point for the classification engine.
A list of tweets is sent via HTTP and sentiment polarity classifications
are returned.


Tweets must be a JSON-encoded mapping from tweetID to tweet text:

`{ "345": "I like kittens :)" }`

This JSON-encoded mapping is then passed to the server in the "tweets"
parameter.

`wget http://localhost:8080/?tweets="%7B%20%22345%22%3A%20%22I%20like%20kittens%20%3A)%22%20%7D"`

Note that by default, an additional "password" parameter is needed. See source.

The server will return a JSON-encoded mapping from tweetID to
sentiment polarity:

`{ "345" : "positive" }`


See client.py for example code.

-- Michael Haas <haas@computerlinguist.org>, 20120503


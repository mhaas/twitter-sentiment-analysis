TaggerServer: Preprocessing
============================


TaggerServer implements preprocessing:

* tokenization

* emoticon detection

* preliminary sentiment analysis via sentiment dictionary


Input is a raw tweet.
Output is a JSON object containing a tokenized version of the tweet
as well as various statistics.

See test.pl for sample client.


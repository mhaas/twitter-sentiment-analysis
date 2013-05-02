Classification Server
=====================

A small Servlet wrapper around WEKA and our trained model.

Start the main method of the ServLet class and send PUT requests to
localhost:8080. The PUT request must contain a JSON dictionary
mapping tweet IDs to a complete ARFF file. Each ARFF file can only contain
one tweet.

The JSON response is a dictionary mapping tweet IDs to the sentiment polarity.

Example code can be found in the TestServLet class.

You might have to adjust some paths in the code.



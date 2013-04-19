Feature extraction module
=========================

This module extracts features from tweets for machine learning purposes.
The features are saved both as CSV files and as ARFF files, ready for
consumption by Weka.

Feature selection is configured by adding and removing extractors
in main.py and main-gold.py.

Tweets from CSV files as well as some manually annotated data sets
provided by the research community are supported.

Extractors live in the extractors/ subdirectory.
Tweet sources live in the tweetloaders/ subdirectory.



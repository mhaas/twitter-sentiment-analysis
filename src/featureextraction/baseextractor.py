#-*- coding: utf-8 -*-


class BaseExtractor(object):

    def __init__(self):
        raise NotImplementedError

  # always returns collections.OrderedDict
    def extractFeatures(self, tweet):
        raise NotImplementedError

    def getFields(self):
        raise NotImplementedError
   

    


__author__ = 'Charlie Meyer <charlie@charliemeyer.net>'

import re


#might want to change this to UserDict
class hsmodelbase:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        for key in self.dictionary.keys():
            function_name = "get_"+re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str(key)).lower().strip('_')
            value = dictionary[key]
            setattr(self.__class__, function_name, self.__gen_func(value))
            setattr(self.__class__, key, value)

    def __gen_func(self, value):
        def fun(self):
            return value
        return fun

class LiveStream(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)

class Score(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)

class Location(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)

class OnDemand(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)
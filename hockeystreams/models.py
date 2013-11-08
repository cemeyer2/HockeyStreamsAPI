__author__ = 'Charlie Meyer <charlie@charliemeyer.net>'

import re, pprint


#might want to change this to UserDict
class hsmodelbase:

    def __init__(self, ind):
        self.dictionary = {}
        for key in ind.keys():
            #https://djangosnippets.org/snippets/585/
            uscore =  re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str(key)).lower().strip('_')
            self.dictionary[uscore] = ind[key]

        for key in self.dictionary.keys():
            function_name = "get_"+ key
            value = self.dictionary[key]
            setattr(self.__class__, function_name, self.__gen_func(value))
            setattr(self.__class__, key, value)

    def __gen_func(self, value):
        def fun(self):
            return value
        return fun

    def __repr__(self):
        s = "<"+str(self.__class__.__name__)+">\n"
        s += pprint.pformat(self.dictionary)
        s += "\n</"+str(self.__class__.__name__)+">"
        return s

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

class OnDemandStream(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)

class Highlight(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)

class CondensedGame(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)

class Team(hsmodelbase):
    def __init__(self, dictionary):
        hsmodelbase.__init__(self, dictionary)
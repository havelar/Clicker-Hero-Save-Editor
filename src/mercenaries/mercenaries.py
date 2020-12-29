import json
from .mercenary import Mercenary

class Mercenaries(list):
    __mercenaries = []
    
    def __init__(self, mercenaries):
        if all(isinstance(mercenary, Mercenary) for mercenary in mercenaries): # Receive Mercenay as OBJ
            self.__mercenaries = mercenaries
        else:
            if 'mercenaries' in mercenaries.keys(): # In case its one level top
                mercenaries = mercenaries['mercenaries']
            if all(isinstance(mercenary, dict) for mercenary in mercenaries.values()): # Receive Mercenay as Dict
                self.__mercenaries = Mercenary.fromParent(mercenaries)
    
    def __getitem__(self, index):
        return self.__mercenaries[index]
    
    def __iter__(self):
        for merc in self.__mercenaries:
            yield merc

    def __str__(self):
        return '< Mercenaries: {0} >'.format(str(len(self.__mercenaries)))
    
    def __repr__(self):
        return '< Mercenaries: {0} >'.format(str(len(self.__mercenaries)))

    @property
    def mercs(self):
        return self.__mercenaries
import base64, zlib, hashlib
import json, re

class CH:
    '''
        .Class to decode, edit and encode Clicker Hero save file.
        
        .Save file use this format:
            SaveFile = 32 bit hash + b64encodedPart
            
        .Working and tested in version: 1.0e12
        .Created by: Henrique Amaral
        .Check for more information:
            - https://clickerheroes.fandom.com/wiki/Save_file
    '''
    
    # Update Game Path in here
    __path = r'/mnt/c/Program Files (x86)/Steam/steamapps/common/Clicker Heroes/clickerHeroSave.txt'
    __hash = hashlib.md5('zlib'.encode("utf-8")).hexdigest() # For some reason this is the only hash it accept..
    __encoded = ''
    __decoded = {}
    
    def __init__(self, txt=None, path=None):
        '''
            If txt is received, use it. Other wise will use passed value or default one.
        '''
        if txt is None:
            if path is None:
                path = self.__path
            with open(path, 'r') as file:
                txt = file.read()
        
        self.__hash = txt[:32]
        self.__encoded = txt[32:]
        
        self.__decode( self.__encoded )
    
    def __decode(self, txt):
        '''
            Decode string save file to Dict
        '''
        self.__decoded = json.loads(zlib.decompress(base64.b64decode(txt)))
    
    def encode(self, replace=False):
        '''
            Encode decoded JSON to be loaded in game
        '''
        dumps = json.dumps(self.__decoded, ensure_ascii=True, separators=(',', ':'))
        xdumps = zlib.compress(dumps.encode("utf-8"))
        xdumps = base64.b64encode(xdumps).decode()
        xdumps = self.__hash + xdumps
        if replace:
            self.__encoded = xdumps
        return xdumps

    @property
    def decoded(self):
        return self.__decoded
    @decoded.setter
    def decoded(self, val: dict):
        self.__decoded = val
        
    @property
    def encoded(self):
        return self.__encoded
    @property
    def hash(self):
        return self.__hash
    
    def pjson(self, indent=4, sort_keys=True):
        '''Just to pretty print'''
        print(json.dumps(self.decoded, indent=indent, sort_keys=sort_keys))
    
    ######## JSON SHORTCUTS ########
    
    @property
    def account(self):
        return self.__decoded['account']
    @account.setter
    def account(self, val: dict):
        for key in self.__decoded['account'].keys():
            if not key in val.keys():
                raise ValueError('Account must have every key needed.')
        self.__decoded['account'] = val
    
    @property
    def gold(self):
        return self.__decoded['gold']
    @gold.setter
    def gold(self, val: str):
        if re.search(r'\d\.\d+e\d+', val): # 1.0e100
            self.__decoded['gold'] = val
    
    @property
    def rubies(self):
        return self.__decoded['rubies']
    @rubies.setter
    def rubies(self, val: int):
        self.__decoded['rubies'] = val
    
    @property
    def achievements(self):
        return self.__decoded['achievements']
    @achievements.setter
    def achievements(self, val: dict):
        self.__decoded['achievements'] = val
    
    @property
    def candyCanes(self):
        return self.__decoded['candyCanes']
    @candyCanes.setter
    def candyCanes(self, val: int): # 
        self.__decoded['candyCanes'] = val
        # Mimic "Max amount earned" 
        self.__decoded['candyCanesEarned'] = round(val + val/1.7894)
    
    @property
    def autoclickers(self):
        return self.__decoded['autoclickers']
    @autoclickers.setter
    def autoclickers(self, val: int):
        self.__decoded['autoclickers'] = val
    
    @property
    def mercenaries(self):
        return list(self.__decoded['mercenaries']['mercenaries'].values())
    @mercenaries.setter
    def mercenaries(self, mercs: list):
        for ind, merc in enumerate(mercs):
            self.__decoded['mercenaries']['mercenaries'][str(ind)] = merc
            
        self.__decoded['mercenaryCount'] = len(mercs)
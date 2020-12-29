from datetime import datetime, timedelta
from ..db.DAO import ch_DAO
import json

class Mercenary():
    __infos = {}

    def __init__(self, phrase1, roller, phrase2, createTime, slotId, creationQuipped, lastQuestStartTime,
                bonusLives, lastQuestDuration, timeToDie, name, lastQuestRewardType, hasUpdate, assetId,
                rarity, updateChecked, lastQuestGoldRewardQty, lastQuestSuccessChance, level, lastQuestRewardQty,
                questResult, statId, experience
                ):
        
        self.__infos = {
            'name': name,
            'level': level,
            'slotId': slotId,
            'timeToDie': timeToDie,
            'statId': statId,
            'assetId': assetId,
            'rarity': rarity,
            'experience': experience,

            'bonusLives': bonusLives,
            'phrase1': phrase1,
            'phrase2': phrase2,
            'roller': roller,
            'createTime': createTime,
            'creationQuipped': creationQuipped,
            'lastQuestStartTime': lastQuestStartTime,
            'lastQuestDuration': lastQuestDuration,
            'lastQuestRewardType': lastQuestRewardType,
            'hasUpdate': hasUpdate,
            'updateChecked': updateChecked,
            'lastQuestGoldRewardQty': lastQuestGoldRewardQty,
            'lastQuestSuccessChance': lastQuestSuccessChance,
            'lastQuestRewardQty': lastQuestRewardQty,
            'questResult': questResult
        }

    def __timeSpanMs(self, ms):
        '''
            Convert milliseconds timestamp to string
        '''
        return datetime.fromtimestamp(ms/1000.0).strftime("%H:%M:%S - %d/%m/%Y")
    
    def __levelConverter(self, uid=None, name=None):
        '''
            Converter INT Mercenary lvl to string or vice-versa. 
        '''
        if uid and not name:
            if uid > 8:
                return 'Demigod +{0}'.format(uid-8)
            SQL = 'select name from mercs_levels where uid = {0}'.format(str(uid))
        elif name and not uid:
            SQL = 'select uid from mercs_levels where name = {0}'.format(str(name))
            
        with ch_DAO() as con:
            con.execute(SQL)
            resp = con.fetchone()[0]
        return resp
    
    def __rarityConverter(self, uid=None, name=None):
        '''
            Converter INT Mercenary rarity to string or vice-versa. 
        '''
        if uid and not name:
            SQL = 'select name from mercs_rarity where uid = {0}'.format(str(uid))
        elif name and not uid:
            SQL = 'select uid from mercs_rarity where name = {0}'.format(str(name))
            
        with ch_DAO() as con:
            con.execute(SQL)
            resp = con.fetchone()[0]
        return resp
    
    def __statIdConverter(self, uid=None, name=None):
        '''
            Converter INT Mercenary statId to string or vice-versa. 
        '''
        if uid and not name:
            SQL = 'select name from mercs_stat where uid = {0}'.format(str(uid))
        elif name and not uid:
            SQL = 'select uid from mercs_stat where name = {0}'.format(str(name))
            
        with ch_DAO() as con:
            con.execute(SQL)
            resp = con.fetchone()[0]
        return resp
    
    def __questConverter(self, uid=None, name=None):
        '''
            Converter INT Mercenary quest type to string or vice-versa. 
        '''
        if uid and not name:
            SQL = 'select name from mercs_quest where uid = {0}'.format(str(uid))
        elif name and not uid:
            SQL = 'select uid from mercs_quest where name = {0}'.format(str(name))
            
        with ch_DAO() as con:
            con.execute(SQL)
            resp = con.fetchone()[0]
        return resp
    
    @classmethod
    def fromParent(cls, mercenaries):
        return [cls(**mercenary) for mercenary in mercenaries.values()]

    @property
    def info(self):
        return self.__infos

    def __str__(self):
        return "< Mercenary {0} >".format(self.__infos['name'])
    def __repr__(self):
        return "< Mercenary {0} >".format(self.__infos['name'])


    # {
    #     'name': self.__name,
    #     'level': self.__levelConverter(self.__level),
    #     'rarity': self.__rarityConverter(self.__rarity),
    #     'stat': self.__statIdConverter(self.__statId),
    #     'timeToDie': str(timedelta(seconds=self.__timeToDie)),
    #     'currentQuest': self.__questConverter(self.__lastQuestRewardType),
    #     'currentQuestDuration': str(timedelta(seconds=self.__lastQuestDuration)),
    #     'currentQuestStart': self.__timeSpanMs(self.__lastQuestStartTime),
    #     'createTime': self.__timeSpanMs(self.__createTime)
    # }
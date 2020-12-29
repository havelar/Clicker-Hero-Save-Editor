import sqlite3

class ch_DAO:
    '''
        cursor.execute('SQL')
        cursor.executeMany("INSERT INTO 'table' VALUES (?,?)", [('a','b'), ('1','2')])
    '''
    __conn = None
    __cursor = None
    __to_commit = None
    
    def __init__(self, dbPath='/home/henrique/WorkSpace/CH_SaveEditor/Clicker-Hero-Save-Editor/src/db/ClickerHerosDB', to_commit=True):
        self.__conn = sqlite3.connect(dbPath)
        self.__cursor = self.__conn.cursor()
        self.__to_commit = to_commit
    
    def __enter__(self):
        return self.__cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__to_commit:
            self.__conn.commit()
        self.__conn.close
        
    @property
    def connection(self):
        return self.__conn
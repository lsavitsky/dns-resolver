from enum import Enum
from collections import defaultdict

class AuthMapper(Enum):
    
    def __init__(self) -> None:
        self.file="/domain/redpanda.cache"
        self.map = self.create_dyn_enum()
        

    def read_cache_save_dic(self):
        res = defaultdict(dict) # initialize dic of records

        with open (self.file, 'r') as feed:
            line = feed.readline()
            if line[0]!=';':
                lineList=line.split(" ")
                rootserver, num, record, IPdest= lineList[0], lineList[1], lineList[2], lineList[3]
                res[rootserver][record] = (IPdest) # each record is a key in corresponding rootserver
                res[rootserver]['num'] = num # extra num attribute

        return res
    
    def create_dyn_enum(self):
        res = self.read_cache_save_dic()
        key = res.keys()[0]
        return Enum(key, res[key])
    




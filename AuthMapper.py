from enum import Enum
from collections import defaultdict

file = "domain/redpanda.cache"
class AuthMapper(Enum):
    
    def __init__(self) -> None:
        self.map = self.create_dyn_enum()
        
    @staticmethod
    def read_cache_save_dic(file : str):
        res = defaultdict(dict) # initialize dic of records

        with open (file, 'r') as feed:
            while True:
                line = feed.readline()
                if not line:
                    break
                
                if line[0] != ';' and  line[0] != '.':
                    lineList=line.split()
                    
                    rootserver, num, record, IPdest = lineList[0], lineList[1], lineList[2], lineList[3]
                    
                    if res[rootserver].get('record'):
                        res[rootserver]['record'][record] = IPdest
                    else:
                        res[rootserver]['record'] = {record: IPdest} # initialize it
                        res[rootserver]['num'] = num # only need to set it once

        return res
    
    def create_dyn_enum(file : str):
        res = AuthMapper.read_cache_save_dic(file)
        res2 = {}
        
        for key, value in res.items():
            print(key, value['record'], value['num'])
            record = Enum('record', ((key, val) for key, val in value['record'].items()))
            num = Enum('num', ('num', str(value['num'])))
            #print("A RECORD:", record.AAAA.value) #EXAMPLE DONT DELETE
            print("enum stuff: ", Enum('record', ((key, val) for key, val in value['record'].items())))
            print("num stuff", num.num.value)
            res2[key] = Enum('AuthMapper', [record, num]) # add root servers to the hashmap
            
            # # first 
            # ls = []
            
            # for innerKey, innerValue in value.items():
            #     if innerKey == 'num':
            #         ls.append(Emum('num', innerValue))
            #     else:
            #         ls.append(Emum('record', innerValue))
                    
            
        print(list(res2["A.ROOT-SERVERS.NET."]))
        return res2
    
cacheDic = AuthMapper.create_dyn_enum( file)

print(cacheDic['A.ROOT-SERVERS.NET.'])






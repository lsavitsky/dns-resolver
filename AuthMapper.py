from enum import Enum
from collections import defaultdict
"""
    *** ENUM TYPE LASS FOR AUTH MAPPER ***
    ** IP ADDRESS -> RECORD TYPE -> IP **

    The AuthMapper is a dictonary with RootServers as keys and their correspondung enumerations as the values.
    There are three eneumeration types: A, AAAA, and Num. 

    To access the record enumeration do AuthMapper[rootserver_key].A.value or AuthMapper[rootserver_key].AAAA.value
    or AuthMapper[rootserver_key].Num.value
"""
class AuthMapper:
    def __init__(self, file: str) -> None:
        self.file = file
        self.map = self.create_dyn_enum()

    @staticmethod
    def read_cache_save_dic(file: str):
        """ This function reads the cache file and saves the records in a dictionary
        :param file: file path
        :return: dictionary with rootserver as key and record as value
        """
        res = defaultdict(dict)  # Initialize dict of records

        with open(file, 'r') as feed:
            while True:
                line = feed.readline()
                if not line:
                    break

                if line[0] != ';' and line[0] != '.':
                    lineList = line.split()
                    rootserver, num, record, IPdest = lineList[0], lineList[1], lineList[2], lineList[3]

                    if 'record' in res[rootserver]:
                        res[rootserver]['record'][record] = IPdest
                    else:
                        res[rootserver]['record'] = {record: IPdest}  # Initialize it
                        res[rootserver]['num'] = num  # Only set it once

        return res

    def create_dyn_enum(self):
        """ This function creates the dynamic enumeration.
        You can access the enumeration by AuthMapper[rootserver_key].A.value
        The number of records is stored in AuthMapper[rootserver_key].Num.value
        
        :return: dictionary with rootserver as key and enumeration as value
        """
        res = self.read_cache_save_dic(self.file)
        dynamic_enums = {}

        for key, value in res.items():
            new_dic = value['record']
            new_dic['Num'] = value['num']
            dynamic_enums[key] = Enum(f"{key}", new_dic)

        return dynamic_enums
    
def main ():
    file = "domain/redpanda.cache"
    auth_mapper = AuthMapper(file).map

    for rootserver in auth_mapper.keys():
        print(auth_mapper[rootserver].A.value)
        print(auth_mapper[rootserver].AAAA.value)
        print(auth_mapper[rootserver].Num.value)
    
##For testing purposes 
# domain file
if __name__ == "__main__": 
    main()
    


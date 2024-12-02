from enum import Enum
from collections import defaultdict

class AuthMapper:
    def __init__(self, file: str) -> None:
        self.file = file
        self.map = self.create_dyn_enum()

    @staticmethod
    def read_cache_save_dic(file: str):
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
        res = self.read_cache_save_dic(self.file)
        dynamic_enums = {}

        for key, value in res.items():
            record_enum = Enum(f"{key}_Record", value['record'])
            num_enum = Enum(f"{key}_Num", {'Num': value['num']})
            dynamic_enums[key] = {'record': record_enum, 'num': num_enum}

        return dynamic_enums
    
# domain file
file = "domain/redpanda.cache"
auth_mapper = AuthMapper(file)

for rootserver, enums in auth_mapper.map.items():
    print(f"Rootserver: {rootserver}")
    print(f"Records Enum: {list(enums['record'])}")
    print(f"Num Enum: {list(enums['num'])}")

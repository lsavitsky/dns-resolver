from enum import Enum
from collections import defaultdict


class AuthMapper:
    """
    \nAuthMapper maintains a dictionary of root servers and their corresponding records.
    \nRecords are dynamically converted into enumerations (A, AAAA, ttl, NS, etc.).
    
    Example:
        To access the enumeration:
        AuthMapper.Direct.value[rootserver_key].A.value
        AuthMapper.Direct.value[rootserver_key].AAAA.value
        AuthMapper.Direct.value[rootserver_key].ttl.value
        
        To access the TLD enumeration:
        AuthMapper.TLD.value[rootserver_key].A.value
        AuthMapper.TLD.value[rootserver_key].AAAA.value
        AuthMapper.TLD.value[rootserver_key].NS.value
        AuthMapper.TLD.value[rootserver_key].ttl.value
    """
    def __init__(self, file: str) -> None:
        self.file = file
        self.map = self.create_dyn_enum()


    @staticmethod
    def read_cache_save_dic(file: str):
        """
        \nReads the cache file and saves the records in a dictionary.
        \nThis function raises an exception if the record type is invalid or the line is invalid.

        :param file: File path to the DNS cache.
        :return: Dictionary with root server as key and records as values.
        """
        res = defaultdict(dict)

        # deafult kets
        res['TLD'] = {}
        res['Direct'] = {}
        
        data = {"TLD": defaultdict(dict), "Direct" : defaultdict(dict)} # enums for the TLD and Domains
        
        category = ('Direct', None)
        
        with open(file, 'r') as feed:
            for line in feed:
                if line.startswith(';') or not line.strip():
                    continue  # Skip comments and empty lines

                line_list = line.split()

                if len(line_list) != 4:
                    raise InvalidCacheLineError(f"Invalid line: {line}")

                rootserver, ttl, record, ip_dest = line_list
                
                if record == "NS": # handle the NS record
                    if rootserver == ".":
                        category = ('Direct', None) 
                    else:
                        category = ('TLD', rootserver)

                elif record in {"A", "AAAA"}: # handle the A and AAAA records
                    if category[0] == "TLD":
                        res.setdefault(category[0], {})
                        res[category[0]].setdefault(category[1], {
                            "NS": rootserver, # set the NS record
                            "ttl": ttl,
                            "record": {}
                        })
                        
                        rootserver = category[1] # set the rootserver to the TLD type (e.g. ORG.)

                    elif category[0] == "Direct":
                        res.setdefault(category[0], {})
                        res[category[0]].setdefault(rootserver, {
                            "record": {},
                            "ttl": ttl
                        })

                    res[category[0]][rootserver]["record"][record] = ip_dest # set the record type to the ip_dest

                else:
                    raise InvalidRecordTypeError(record)
        return res

    def create_dyn_enum(self):
        """
        \nCreates dynamic enumerations for root server records.

        \nEach root server key maps to an enum containing record types (A, AAAA, NS, etc.)
        \nand the number of records (ttl).

        :return: Dictionary with root server as key and enumeration as value.
        
        >>> auth_mapper = AuthMapper("dns_caches/root.cache").create_dyn_enum()
        ... #####print(auth_mapper.TLD.value['ORG.'].NS.value)
        ORG-TLD.DNS.NET.
        """
        cache_data = self.read_cache_save_dic(self.file) # read the cache file and save the records in a dictionary

        catgory_data = {} # create the category data
        
        for category, values in cache_data.items():
            catgory_data[category] = {}
            
            for rootserver, records in values.items():
                enum_data = {}
                if "record" in records:
                    enum_data.update(records["record"])
                    enum_data["ttl"] = records["ttl"]
                    
                    if category == 'TLD': # add the NS record to the TLD
                        enum_data['NS'] = records['NS']
                else:
                    raise ValueError(f"No valid records found for root server: {rootserver}")
                
                catgory_data[category][rootserver] = Enum(f"{rootserver}", enum_data) # create the enum for the rootserver

        return Enum("Category", catgory_data) # return the enum
    
    
def main ():
    file = "dns_caches/root.cache"
    auth_mapper = AuthMapper(file).map

    print(auth_mapper.TLD.value['ORG.'].NS.value)
    # print(auth_mapper['.'].keys())
    # print(auth_mapper['.']['redpanda.NET.'].A.value)
    # print(auth_mapper['TLD'].keys())

if __name__ == "__main__": 
    main()
    



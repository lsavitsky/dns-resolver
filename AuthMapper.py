from enum import Enum
from collections import defaultdict


class AuthMapper:
    """
    AuthMapper maintains a dictionary of root servers and their corresponding records.
    Records are dynamically converted into enumerations (A, AAAA, ttl, etc.).
    For root server '.', the enumeration contains NS records, such that AuthMapper['.'].NS.value
    returns the list of TLD servers and their corresponding number.

    Example:
        To access the enumeration:
        AuthMapper[rootserver_key].A.value
        AuthMapper[rootserver_key].AAAA.value
        AuthMapper[rootserver_key].ttl.value
        
        For root server '.':
        AuthMapper['.'].NS.value[0]  # First TLD server number
        AuthMapper['COM.'].NS.value = rootserver_key 
        
        
        AuthMapper['Domain'].A
        AuthMapper['tld'].A
        
        AuthMapper[AuthMapper['.'].NS.value[0]].A.value        
        
        
        {
        enum = {DOMAINS, TLDS}
        AuthMapper['.'].COM.value
        '.'= DOMAIN for webserver
        DOMAIN -> rootserver_key.A.value
        
        
        AuthMapper['COM.']
        
        '.COM' = DOMAIN for TLD Server
        DOMAIN -> rootserver_key.A.value
        
        rootserver_key = Domain looking to go to OR the next link for location aka the domain of the TLD server
     ------------

-----------------------------------
    AuthMapper ={
            '.' :{ 
                'redpanda.NET': { A: , AAAA:, ttl: }
                 'redpandas.NET': { A: , AAAA:, ttl: }
            }
            'TLD': {
                'NET.': { A: , AAAA:, ttl: },
                'ORG.': { A: , AAAA:, ttl: },
        }
        
    AuthMapper['.']['redpanda.NET'].A.value
    AuthMapper['TLD']['NET.'].A.value
    AuthMapper.TLD <- Want
    AuthMapper.. <-Uhhh change . to domain when read in?
    """
    def __init__(self, file: str) -> None:
        self.file = file
        self.map = self.create_dyn_enum()


    @staticmethod
    def read_cache_save_dic(file: str):
        """
        Reads the cache file and saves the records in a dictionary.
        This function raises an exception if the record type is invalid or the line is invalid.

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
                # print(line_list)

                if len(line_list) != 4:
                    raise InvalidCacheLineError(f"Invalid line: {line}")

                rootserver, ttl, record, ip_dest = line_list
                
                if record == "NS":
                    if rootserver == ".":
                        category = ('Direct', None)
                    else:
                        category = ('TLD', rootserver)

                elif record in {"A", "AAAA", "NS"}:
                    if category[0] == "TLD":
                        res.setdefault(category[0], {})
                        res[category[0]].setdefault(category[1], {
                            "NS": rootserver,
                            "ttl": ttl,
                            "record": {}
                        })
                        
                        rootserver = category[1]

                    elif category[0] == "Direct":
                        res.setdefault(category[0], {})
                        res[category[0]].setdefault(rootserver, {
                            "record": {},
                            "ttl": ttl
                        })

                    res[category[0]][rootserver]["record"][record] = ip_dest

                else:
                    raise InvalidRecordTypeError(record)
        return res

    def create_dyn_enum(self):
        """
        Creates dynamic enumerations for root server records.

        Each root server key maps to an enum containing record types (A, AAAA, NS, etc.)
        and the number of records (ttl).

        :return: Dictionary with root server as key and enumeration as value.
        """
        cache_data = self.read_cache_save_dic(self.file)

        catgory_data = {}
        
        for category, values in cache_data.items():
            catgory_data[category] = {}
            
            for rootserver, records in values.items():
                enum_data = {}
                if "record" in records:
                    enum_data.update(records["record"])
                    enum_data["ttl"] = records["ttl"]
                    
                    if category == 'TLD':
                        enum_data['NS'] = records['NS']
                else:
                    raise ValueError(f"No valid records found for root server: {rootserver}")
                
                catgory_data[category][rootserver] = Enum(f"{rootserver}", enum_data)

        return Enum("Category", catgory_data)
    
    
def main ():
    file = "dns_caches/root.cache"
    auth_mapper = AuthMapper(file).map

    print(auth_mapper.TLD.value['ORG.'].NS.value)
    # print(auth_mapper['.'].keys())
    # print(auth_mapper['.']['redpanda.NET.'].A.value)
    # print(auth_mapper['TLD'].keys())

if __name__ == "__main__": 
    main()
    



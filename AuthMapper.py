from enum import Enum
from collections import defaultdict
import sys

class AuthMapper:
    """
    AuthMapper maintains a dictionary of root servers and their corresponding records.
    Records are dynamically converted into enumerations (A, AAAA, Num, etc.).
    For root server '.', the enumeration contains NS records, such that AuthMapper['.'].NS.value
    returns the list of TLD servers and their corresponding number.

    Example:
        To access the enumeration:
        AuthMapper[rootserver_key].A.value
        AuthMapper[rootserver_key].AAAA.value
        AuthMapper[rootserver_key].Num.value
        
        For root server '.':
        AuthMapper['.'].NS.value[0]  # First TLD server number
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

        with open(file, 'r') as feed:
            for line in feed:
                if line.startswith(';') or not line.strip():
                    continue  # Skip comments and empty lines

                line_list = line.split()
                if len(line_list) != 4:
                    raise InvalidCacheLineError(line)

                rootserver, num, record, ip_dest = line_list

                if record == "NS":
                    res[rootserver].setdefault("NS", {})[ip_dest] = num
                elif record in {"A", "AAAA"}:
                    record_data = res[rootserver].setdefault("record", {})
                    record_data[record] = ip_dest
                    res[rootserver]["num"] = num  # Store the number of records
                else:
                    raise InvalidRecordTypeError(record)
        return res


    def create_dyn_enum(self):
        """
        Creates dynamic enumerations for root server records.

        Each root server key maps to an Enum containing record types (A, AAAA, NS, etc.)
        and the number of records (Num).

        :return: Dictionary with root server as key and enumeration as value.
        """
        cache_data = self.read_cache_save_dic(self.file)
        dynamic_enums = {}

        for rootserver, records in cache_data.items():
            enum_data = {}
            if "record" in records:
                enum_data.update(records["record"])
                enum_data["Num"] = records["num"]
            elif "NS" in records:
                enum_data["NS"] = records["NS"]
            else:
                raise ValueError(f"No valid records found for root server: {rootserver}")

            dynamic_enums[rootserver] = Enum(f"{rootserver}", enum_data)

        return dynamic_enums
    
def main ():
    file = "dns_caches/root.cache"
    auth_mapper = AuthMapper(file).map

    for rootserver in auth_mapper.keys():
        if rootserver != '.':
            print(auth_mapper[rootserver].A.value)
            print(auth_mapper[rootserver].AAAA.value)
            print(auth_mapper[rootserver].Num.value)
            
        else:
            print(auth_mapper[rootserver].NS.value)

if __name__ == "__main__": 
    main()
    


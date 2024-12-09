from dns_transaction_and_counts import dns_transaction_ID 
from dns_transaction_and_counts import dns_counters
from dns_query_flag import *


class dns_header:
    """
    dns_construction/
    Overall header creation using
    - dns_query_flag.py (a bunch of enums)
    - dns_transactions_and_counts (combination of 2 classes)
    """
    def __init__(self, transation_id= None, flags=0, counts =None):
        """
        To change later for more use but now its default... 
        """
        self.transaction_id = dns_transaction_ID.random_ID() 
        self.flags= flags
        self.counters= dns_counters() #First it is default
         
        
    def byte_format_construction(self)-> bytes:
        return(
            self.transaction_id.to_bytes(2, "big")+
            self.flags.to_bytes(2,"big") +
            self.counters.bytes_format()
        )


def runtests():
    print(dns_header().byte_format_construction())
             
if __name__ == "__main__":
    runtests()
    
    
    #Actually needs testing... minimal for counts and transaction integration      
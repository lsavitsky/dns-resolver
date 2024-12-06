"""
Refence: https://www.iana.org/domains/root/files    - for the root file
"""
from dnslib import DNSRecord, DNSError, QTYPE, RCODE, RR
import AuthMapper
from pathlib import Path
import sys
import DNS_resolver

sys.path.append("../dns_caches/")

# This is a simple DNS resolver that can resolve certain types of DNS queries.s
class DNS_ISP_resolver(Resolver ):
    """
    ISP DNS resolver. Resolves queries using a ISP cache,
    falling back to the main resolver if necessary.
    """
    DOMAIN_TO_IP={}
    
    def __init__(self, file: Path = Path("ISP.cache")):
        # used to save the domains
        self.file_cache = file
        self.ISP_map = self.read_dns_cache(self.file_cache)

    def getLevelMap(self):
        return self.map
    def getNextLevelMap(self):
        super()
        
        
    def read_dns_cache(self, file : str):
        """
            read_dns_cache attempts to read from the cache file and creates an
            enum type AuthMapper
            
            :param: file: - the location of the cache
        """
        try:
            return AuthMapper(file).map
        except Exception as e:
            print(f"Error reading DNS cache file: {e}")
            return {}
        
        
        
    
    
    
    
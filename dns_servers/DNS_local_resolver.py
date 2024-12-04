"""
Refence: https://www.iana.org/domains/root/files    - for the root file
"""
from dnslib import DNSRecord, DNSError, QTYPE, RCODE, RR
import AuthMapper
import DNS_ISP_resolver
import sys 
from pathlib import Path

sys.path.append("../dns_caches/")

# This is a simple DNS resolver that can resolve certain types of DNS queries.s
class DNS_Local_resolver(DNS_ISP_resolver):
    """
    This class is a simple DNS resolver that can resolve certain types of DNS queries.
    It is designed to be used with an object of the class.
    """
    
    def __init__(self, file: Path = Path("local.cache")):
        # used to save the domains
        super().__init__() # INHERIT all of the methods
        
        self.file_cache = file
        self.Local_map = self.read_dns_cache(self.file_cache)
        
        
    def check_dns(self, domain):
        """
        Check for the dns inside of the map. if it exists yay.
        if not then super the parent ISP
        """

        if self.Local_map.get(domain):
            return self.Local_map[domain]
        
        super().__init__()
        return self.ISP_map.get(domain, "NXDOMAIN")
        
    def read_dns_cache(self, file : str):
        """
            read_dns_cache attempts to read from the cache file and creates an
            enum type AuthMapper
            
            :param: file: - the location of the cache
        """
        try: #check if file exists etc...
            return AuthMapper(file).map
        except Exception as e:
            print(f"Error reading DNS cache file: {e}")
            return {}
        
        
        
    
    
    
    
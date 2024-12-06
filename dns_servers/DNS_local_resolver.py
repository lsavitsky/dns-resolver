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
    def __init__(self, local_file: Path = Path("local.cache"), isp_file: Path = Path("ISP.cache")):
        """
        Initialize the local resolver with its own cache and the ISP resolver's cache.
        """
        
        super().__init__(isp_file) # Initialize ISP resolver (for fallback)

        # Load local cache
        self.Local_map = self.read_dns_cache(local_file)
    
    def resolve(self, domain: str) -> str:
        """
        Check for the dns inside of the map. if it exists yay.
        if not then super the parent ISP
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        if domain in self.Local_map:
            return self.Local_map[domain]
        return super().resolve(domain)  # Use ISP resolver as fallback
           
    # def resolve(self, file : str):
    #     """
    #     read_dns_cache attempts to read from the cache file and creates an
    #     enum type AuthMapper
        
    #     :param: file: - the location of the cache
    #     """
    #     try: #check if file exists etc...
    #         return AuthMapper(file).map
    #     except Exception as e:
    #         print(f"Error reading DNS cache file: {e}")
    #         return {}
    
     
    
    
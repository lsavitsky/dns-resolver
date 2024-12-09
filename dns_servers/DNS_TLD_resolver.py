from dnslib import DNSRecord, DNSError, QTYPE, RCODE, RR
from pathlib import Path
from DNS_resolver import Resolver
from enum import Enum
import sys 

TLD_MAPS = Path('../dns_caches/tld_mappings/')
AUTH_CACHES = Path('../dns_caches/authorative_caches/')
class DNS_TLD_resolver(Resolver):
    """
    ISP DNS resolver. Resolves queries using an ISP cache,
    falling back to the main resolver if necessary.
    """

    def __init__(self, tld_file: Path = Path("tld.cache")):
        """
        Initializes the ISP DNS resolver with a cache file.
        
        :param file: Path to the ISP cache file.
        """
        super().__init__(tld_file)  # inherit initialization from Resolver
        
    def find_tld_file(self, root_response: Enum) -> Path:
        """
        Finds the TLD cache file for a given TLD.
        
        :param tld: The top-level domain to find the cache file for.
        :return: Path to the TLD cache file.
        """
        ip_addresses =  TLD_MAPS / f"ip-addresses-.csv"
        
        A = root_response.A.value
        AAAA = root_response.AAAA.value
        
        # open 
        with open(ip_addresses, 'r') as file:
            for line in file:
                record_type, domain, ip = line.strip().split(',')

                if A == ip: 
                    return AUTH_CACHES / f"{domain}.cache"
                
                if AAAA == ip:
                    return AUTH_CACHES / f"{domain}.cache"
                
        return "tld.cache"
                
        
    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using the ISP cache.
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        res = self.cache_map.Direct.value.get(domain, "NXDOMAIN")
        
        return res
    
    def get_authoritative_file(self, TLD_response: Enum) -> str:
        """
        Returns the authoritative server for a given TLD.
        
        :param tld: The top-level domain to find the authoritative server for.
        :return: The authoritative server for the given TLD.
        """
        
        if TLD_response == "NXDOMAIN":
            return "authoritative.cache"
        
        return self.find_tld_file(TLD_response)

def main():
    isp_resolver = DNS_TLD_resolver()
    
    isp_resolver.print_result(isp_resolver.resolve("google.com"))
    isp_resolver.print_result(isp_resolver.resolve("yahoo.com"))
    isp_resolver.print_result(isp_resolver.resolve("example.com"))
    
    

if __name__ == "__main__":
    main()
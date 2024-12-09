from pathlib import Path
from DNS_resolver import Resolver
from enum import Enum
import sys 

TLD_MAPS = Path('tld_mappings/')

class DNS_TLD_resolver(Resolver):
    """
    ISP DNS resolver. Resolves queries using an ISP cache, 
    falling back to the main resolver if necessary.
    """

    def __init__(self, root_response: Enum):
        """
        Initializes the ISP DNS resolver with a cache file.
        
        :param file: Path to the ISP cache file.
        """
        self.tld_file = super().find_resolver_file(root_response, TLD_MAPS) # get the TLD file based on the root response
        
        print(f"Loading TLD cache file {self.tld_file}...")
        super().__init__(self.tld_file)
        
    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using the ISP cache.
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        
        return self.cache_map.Direct.value.get(domain, "NXDOMAIN")

def main():
    isp_resolver = DNS_TLD_resolver()
    
    isp_resolver.print_result(isp_resolver.resolve("google.com"))
    isp_resolver.print_result(isp_resolver.resolve("yahoo.com"))
    isp_resolver.print_result(isp_resolver.resolve("example.com"))
    
    

if __name__ == "__main__":
    main()
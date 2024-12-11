import re
from pathlib import Path
from collections import defaultdict
from DNS_resolver import Resolver
import sys

sys.path.append("DNS_Query/dns_construction/")
from dns_packet import dns_packet

class DNS_Root_resolver(Resolver):
    """
    Root DNS resolver that provides information about TLD DNS servers.
    """
    def __init__(self, dns_query: dns_packet, root_cache: Path = Path("root.cache")):
        """
        Initializes the Root DNS Resolver by loading the root cache.

        :param root_cache: Path to the root cache file.
        """

        #("Setting up root")
        super().__init__(dns_query, root_cache)
        #print("Root map", self.cache_map)

    def resolve(self) -> dict:
        """
        \nResolves a domain name to the root server information.
        \nIf the domain is not found, then the TLD is extracted 
        \nand used to resolve the root server.
        
        \n If the TLD is not found then 'NXDOMAIN' is returned.
        
        :param domain: The domain name to resolve.
        :return: Root server info or 'NXDOMAIN' 
        """
        domain = self.dns_query.q.qname.domain_name
        direct_result = self.cache_map.Direct.value.get(domain, None)
        #print(f"Resolving {domain} using root cache.")
        if direct_result:
            #print(f"  Found {domain} in root cache.")
            return direct_result
        
        # fallback to the TLD if the domain is not found
        #print(f"  {domain} not found in root cache.")
        #print("Falling back to TLD...")
        tld = domain.split('.')[-2] + '.' # get the TLD
        
        #print(f"Resolving TLD {tld} using root cache.")
        return self.cache_map.TLD.value.get(tld, "NXDOMAIN")
        
def main():
    root_resolver = DNS_Root_resolver()
    root_resolver.print_result(root_resolver.resolve("Paola.ORG.")) 
    
if __name__ == "__main__":
    main()
    

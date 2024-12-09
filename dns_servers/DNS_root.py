import re
from pathlib import Path
from collections import defaultdict
from DNS_resolver import Resolver
import sys

sys.path.append("../dns_caches/")


class DNS_Root_resolver(Resolver):
    """
    Root DNS resolver that provides information about TLD DNS servers.
    """
    def __init__(self, root_cache: Path = Path("root.cache")):
        """
        Initializes the Root DNS Resolver by loading the root cache.

        :param root_cache: Path to the root cache file.
        """
        
        super().__init__(root_cache)

    def resolve(self, domain: str) -> dict:
        """
        \nResolves a domain name to the root server information.
        \nIf the domain is not found, then the TLD is extracted 
        \nand used to resolve the root server.
        
        \n If the TLD is not found then 'NXDOMAIN' is returned.
        
        :param domain: The domain name to resolve.
        :return: Root server info or 'NXDOMAIN' 
        """
        direct_result = self.cache_map.Direct.value.get(domain, None)
        print(f"Resolving {domain} using root cache.")
        if direct_result:
            print(f"  Found {domain} in root cache.")
            return direct_result
        
        # fallback to the TLD if the domain is not found
        print(f"  {domain} not found in root cache.")
        print("Falling back to TLD...")
        tld = domain.split('.')[-2] + '.' # get the TLD
        print(f"Resolving TLD {tld} using root cache.")
        return self.cache_map.TLD.value.get(tld, "NXDOMAIN")
        
def main():
    root_resolver = DNS_Root_resolver()
    root_resolver.print_result(root_resolver.resolve("Paola.ORG."))
    
if __name__ == "__main__":
    main()
    

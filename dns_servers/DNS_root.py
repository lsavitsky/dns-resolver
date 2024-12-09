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
    
    
#### Old code

# @staticmethod
# def parse_root_cache(file: Path) -> dict: # don't need this method but leaving it for now in case I am wrong
#     """
#     Parses the root.cache file to extract TLD mappings.

#     :param file: Path to the root cache file.
#     :return: Dictionary mapping TLDs to their respective root servers.
#     """
#     tld_map = defaultdict(dict)

#     try:
#         with open(file, 'r') as f:
#             lines = f.readlines()

#         for line in lines:
#             if line.strip() and not line.startswith(';'):  # Skip comments
#                 parts = re.split(r'\s+', line.strip())
#                 if len(parts) >= 4:
#                     tld = parts[0]  # TLD or `.` 
#                     record_type = parts[2]
#                     value = parts[3]

#                     if record_type == "NS": # NS record type
#                         tld_map[tld]['NS'] = value
                        
#                     elif record_type in ["A", "AAAA"]: #REcords of A and AAAA
#                         if 'IP' not in tld_map[tld]:
#                             tld_map[tld]['IP'] = []
#                         tld_map[tld]['IP'].append(value) #resolve IP addresses

#     except FileNotFoundError:
#         print(f"Root cache file '{file}' not found.")
#     except Exception as e:
#         print(f"Error parsing root cache file: {e}")

#     return tld_map
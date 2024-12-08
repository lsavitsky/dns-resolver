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
        # self.tld_map = self.parse_root_cache(root_cache)

    @staticmethod
    def parse_root_cache(file: Path) -> dict:
        """
        Parses the root.cache file to extract TLD mappings.

        :param file: Path to the root cache file.
        :return: Dictionary mapping TLDs to their respective root servers.
        """
        tld_map = defaultdict(dict)

        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            for line in lines:
                if line.strip() and not line.startswith(';'):  # Skip comments
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) >= 4:
                        tld = parts[0]  # TLD or `.` 
                        record_type = parts[2]
                        value = parts[3]

                        if record_type == "NS": # NS record type
                            tld_map[tld]['NS'] = value
                            
                        elif record_type in ["A", "AAAA"]: #REcords of A and AAAA
                            if 'IP' not in tld_map[tld]:
                                tld_map[tld]['IP'] = []
                            tld_map[tld]['IP'].append(value) #resolve IP addresses

        except FileNotFoundError:
            print(f"Root cache file '{file}' not found.")
        except Exception as e:
            print(f"Error parsing root cache file: {e}")

        return tld_map

    def resolve(self, tld: str) -> dict:
        """
        Resolves a TLD to its root server information.

        :param tld: TLS SERVER ( 'com', 'org').
        :return: Root server info or 'NXDOMAIN' 
        """
        return self.cache_map.get(tld, "NXDOMAIN")
        # return self.tld_map.get(tld, "NXDOMAIN")

def main():
    root_resolver = DNS_Root_resolver()
    print(root_resolver.resolve("A.ROOT-SERVERS.NET."))
    print(root_resolver.resolve("B.ROOT-SERVERS.NET."))
    print(root_resolver.resolve("C.ROOT-SERVERS.NET."))
    
if __name__ == "__main__":
    main()
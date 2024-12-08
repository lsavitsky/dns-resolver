from dnslib import DNSRecord, DNSError, QTYPE, RCODE, RR
from pathlib import Path
from DNS_resolver import Resolver

class DNS_ISP_resolver(Resolver):
    """
    ISP DNS resolver. Resolves queries using an ISP cache,
    falling back to the main resolver if necessary.
    """

    def __init__(self, file: Path = Path("ISP.cache")):
        """
        Initializes the ISP DNS resolver with a cache file.
        
        :param file: Path to the ISP cache file.
        """
        super().__init__(file)  # inherit initialization from Resolver
        self.ISP_map = self.cache_map
        
    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using the ISP cache.
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        return self.ISP_map.get(domain, "NXDOMAIN")

def main():
    isp_resolver = DNS_ISP_resolver()
    print(isp_resolver.resolve("google.com"))
    print(isp_resolver.resolve("example.com"))
    print(isp_resolver.resolve("example.net"))
    

if __name__ == "__main__":
    main()
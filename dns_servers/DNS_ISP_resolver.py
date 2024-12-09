from pathlib import Path
# from DNS_resolver import Resolver
from DNS_safe_resolver import DNS_Safe_Resolver

import sys
sys.path.append("DNS_Query/dns_construction/")
from dns_packet import dns_packet


class DNS_ISP_resolver(DNS_Safe_Resolver):
    """
    ISP DNS resolver. Resolves queries using an ISP cache,
    falling back to the main resolver if necessary.
    """

    def __init__(self, dns_query: dns_packet, file: Path = Path("ISP.cache")):
        """
        Initializes the ISP DNS resolver with a cache file.
        
        :param file: Path to the ISP cache file.
        """
        print("Setting up ISP")
        super().__init__(dns_query, file)  # inherit initialization from Resolver
        self.ISP_map = self.read_dns_cache(file)
    
        
    def resolve(self) -> str:
        """
        Resolves a domain name using the ISP cache.
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """

        domain = self.dns_query.q.qname.domain_name
        
        res = self.ISP_map.Direct.value.get(domain)
        if res:
            return res
        
        return super().resolve()

def main():
    isp_resolver = DNS_ISP_resolver()
    
    isp_resolver.print_result(isp_resolver.resolve("google.com"))
    isp_resolver.print_result(isp_resolver.resolve("yahoo.com"))
    isp_resolver.print_result(isp_resolver.resolve("example.com"))
    
    

if __name__ == "__main__":
    main()
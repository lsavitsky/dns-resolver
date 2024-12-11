"""
Refence: https://www.iana.org/domains/root/files    - for the root file
"""
import sys 
from pathlib import Path
from DNS_ISP_resolver import DNS_ISP_resolver

sys.path.append("DNS_Query/dns_construction/")
from dns_packet import dns_packet


# This is a simple DNS resolver that can resolve certain types of DNS queries.s
class DNS_Local_resolver(DNS_ISP_resolver):
    """
    Local DNS resolver. Resolves queries using a local cache,
    falling back to the ISP resolver if necessary.
    """
    def __init__(self, dns_query: dns_packet, local_file: Path = Path("local.cache"), isp_file: Path = Path("ISP.cache")):
        """
        Initialize the local resolver with its own cache and the ISP resolver's cache.
        """
        # print("Setting up Local")
        super().__init__(dns_query, isp_file)  # create the ISP resolver (fallback)
        self.local_cache = self.read_dns_cache(local_file)  # Load the local cache 

        
    def resolve(self) -> str:
        """
        Check for the dns inside of the map. if it exists yay.
        if not then super the parent ISP
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        domain = self.dns_query.q.qname.domain_name

        # attempt to resolve the domain using the local cache
        # print(f"Resolving {domain} using local cache.")
        res = self.local_cache.Direct.value.get(domain)
        if res:
            # print(f"  Found {domain} in local cache.")
            return res  # return res from the local cache

        # print(f"  {domain} not found in local cache.")
        # print("Falling back to ISP resolver...")
        # Fallback to the ISP resolver if not found in the local cache
        return super().resolve()
  
# test the DNS_Local_resolver  
def main():
    resolver = DNS_Local_resolver()
    redPanda = resolver.resolve("redpanda.com")
    resolver.print_result(redPanda)
    
    

if __name__ == "__main__":
    main()
    
    
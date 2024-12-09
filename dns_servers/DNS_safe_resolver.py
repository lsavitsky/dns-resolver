from pathlib import Path
from DNS_resolver import Resolver
from DNS_Recursive_resolver import DNS_Recursive_resolver
import sys

sys.path.append("DNS_Query/dns_construction/")
from DNS_Tunnel_enums import EncodingType
from dns_packet import dns_packet
from dns_question_enum import QNAME

class DNS_Safe_Resolver(DNS_Recursive_resolver):
    """
    ISP DNS resolver. Resolves queries using an ISP cache,
    falling back to the main resolver if necessary.
    """

    def __init__(self, dns_query: dns_packet, file: Path = Path("safe.cache")):
        """
        Initializes the ISP DNS resolver with a cache file.
        
        :param file: Path to the ISP cache file.
        """
        print("Setting up safe")
        super().__init__(dns_query, file)  # inherit initialization from Resolver
        self.safe_map = self.read_dns_cache(file)
        print("Safe set-up done")
        
    def resolve(self) -> str:
        """
        Resolves a domain name using the ISP cache.
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        encoded_domain = self.dns_query.q.qname.domain_name
        decoded_domain = self.dns_query.q.qname.decode_tunnel(encoded_domain)
        result = self.safe_map.Direct.value.get(decoded_domain, "NXDOMAIN")
        # if result == "NXDOMAIN":
            
            # for encodeType in EncodingType.__members__:
            #     EncodingType[encodeType].decode(domain)

            #     res = self.cache_map.Direct.value.get(domain)

            #     if res:
            #         return res
        # super().dns_query = 
        self.dns_query.q.qname.domain_name = decoded_domain
        return super().resolve()

        

                

    
def main():
    isp_resolver = DNS_Safe_Resolver()
    
    isp_resolver.print_result(isp_resolver.resolve("google.com"))
    isp_resolver.print_result(isp_resolver.resolve("yahoo.com"))
    isp_resolver.print_result(isp_resolver.resolve("example.com"))
    
    

if __name__ == "__main__":
    main()
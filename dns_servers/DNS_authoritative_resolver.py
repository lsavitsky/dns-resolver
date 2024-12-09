from DNS_resolver import Resolver
from pathlib import Path
from enum import Enum
import sys

sys.path.append("DNS_Query/dns_construction/")
from dns_packet import dns_packet

AUTH_MAPS = Path('/auth_mappings/')

class DNS_Authoritative_resolver(Resolver):
    """
    Authoritative DNS resolver for a specific zone.
    """
    def __init__(self, dns_query: dns_packet, tld_response: Enum):
        self.auth_file = super().find_resolver_file(tld_response, AUTH_MAPS)
        super().__init__(dns_query, self.auth_file)
        
    def resolve(self) -> str:
        """
        Resolves a domain name using the authoritative cache. 
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        domain = self.dns_query.q.qname.domain_name
        return self.cache_map.Direct.value.get(domain, "NXDOMAIN")
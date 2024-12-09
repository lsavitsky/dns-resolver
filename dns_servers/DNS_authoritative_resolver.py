from DNS_resolver import Resolver
from pathlib import Path
from enum import Enum

AUTH_MAPS = Path('/auth_mappings/')

class DNS_Authoritative_resolver(Resolver):
    """
    Authoritative DNS resolver for a specific zone.
    """
    def __init__(self, tld_response: Enum):
        self.auth_file = super().find_resolver_file(tld_response, AUTH_MAPS)
        super().__init__(self.auth_file)
        
    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using the authoritative cache.
        
        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        return self.cache_map.Direct.value.get(domain, "NXDOMAIN")
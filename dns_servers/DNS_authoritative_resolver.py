from dns_resolver import DNSResolver
from pathlib import Path

class DNS_Authoritative_resolver(DNSResolver):
    """
    Authoritative DNS resolver for a specific zone.
    """
    def __init__(self, file: Path):
        super().__init__(file)
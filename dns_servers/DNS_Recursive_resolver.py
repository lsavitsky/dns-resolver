import socket
from dnslib import DNSRecord, QTYPE, RCODE
from pathlib import Path
from DNS_Local_resolver import DNS_Local_resolver  # isp resolver
from DNS_Root_resolver import DNS_Root_resolver  # root resolver


class RecursiveDNSServer:
    """
    Recursive DNS server that resolves domain names using local, ISP, and root server caches.
    """

    def __init__(self, 
                 local_cache: Path = Path("local.cache"),
                 isp_cache: Path = Path("ISP.cache"),
                 root_cache: Path = Path("root.cache"),
                 port: int = 53):
        """
        Initializes the recursive DNS server.

        :param local_cache: Path to the local DNS cache file.
        :param isp_cache: Path to the ISP DNS cache file.
        :param root_cache: Path to the root DNS cache file.
        :param port: Port to communicate with DNS servers (default is 53).
        """
        self.local_resolver = DNS_Local_resolver()
        self.auth_mapper = DNS_Root_resolver()
        self.port = port
        
    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using the local, ISP, and root DNS resolvers.

        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        pass  # implement this method
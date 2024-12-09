import socket
from dnslib import DNSRecord, QTYPE, RCODE
from pathlib import Path
from DNS_local_resolver import DNS_Local_resolver  # isp resolver
from DNS_root import DNS_Root_resolver  # root resolver

class DNS_Recursive_resolver:
    """
    Recursive DNS server that resolves domain names using local, ISP, and root server caches.
    """
    def __init__(self, root_file: Path = Path("root.cache"), tld_file: Path =Path(""), authoritative_file: Path =Path("")):
        """
        Initializes the recursive DNS server.
        #TODO Fix this docstring
        :param local_cache: Path to the local DNS cache file.
        :param isp_cache: Path to the ISP DNS cache file.
        :param root_cache: Path to the root DNS cache file.
        :param port: Port to communicate with DNS servers (default is 53).
        """
        self.root_resolver = DNS_Root_resolver(root_file)
        self.tld_resolvers = tld_resolvers
        self.authoritative_resolvers = authoritative_resolvers

    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using recursive resolvers.

        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        parts = domain.split('.')
        if len(parts) < 2:
            return "NXDOMAIN" #Enough parts of it neededd

        tld = parts[-1]
        zone = f"{parts[-2]}.{tld}"

        # Query Root Resolver
        root_info = self.root_resolver.resolve(".") # DNS_root.py
        if root_info == "NXDOMAIN":
            return "NXDOMAIN"

        tld_ns = root_info['NS'] #This is the ns root info
        tld_ip = root_info['IP'][0]  #Change for the IP selection desired. right now it is the first one found

        # Query TLD Resolver
        tld_resolver = self.tld_resolvers.get(tld_ns)
        if not tld_resolver:
            return "NXDOMAIN"

        authoritative_ns = tld_resolver.resolve(zone)
        if authoritative_ns == "NXDOMAIN":
            return "NXDOMAIN"

        # Query Authoritative Resolver
        authoritative_resolver = self.authoritative_resolvers.get(authoritative_ns)
        if not authoritative_resolver:
            return "NXDOMAIN"

        return authoritative_resolver.resolve(domain)


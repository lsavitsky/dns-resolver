import socket
from dnslib import DNSRecord, QTYPE, RCODE
from pathlib import Path

# Importing the resolvers
from DNS_root import DNS_Root_resolver  # root resolver
from DNS_TLD_resolver import DNS_TLD_resolver  # tld resolver
from DNS_authoritative_resolver import DNS_authoritative_resolver  # authoritative resolver

class DNS_Recursive_resolver:
    """
    Recursive DNS server that resolves domain names using local, ISP, and root server caches.
    """
    def __init__(self, root_file: Path("root.cache"), tld_file: Path = Path("TLD.cache"), authoritative_file: Path = Path("authorative.cache")):
        """
        Initializes the recursive DNS server.
        #TODO Fix this docstring
        :param local_cache: Path to the local DNS cache file.
        :param isp_cache: Path to the ISP DNS cache file.
        :param root_cache: Path to the root DNS cache file.
        :param port: Port to communicate with DNS servers (default is 53).
        """
        self.root_resolver = DNS_Root_resolver(root_file)
        self.tld_resolvers = DNS_TLD_resolver(tld_file)
        self.authoritative_resolvers = None # this will be set in the resolve method

    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name using recursive resolvers.

        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        parts = domain.split('.')
        if len(parts) < 2:
            return "NXDOMAIN" # Enough parts of it neededd

        tld = parts[-1]
        zone = f"{parts[-2]}.{tld}"

        # Step 1: Query Root Resolver
        root_info = self.root_resolver.resolve(domain)
        if root_info == "NXDOMAIN":
            return "NXDOMAIN"

        if not root_info.hasattr('NS'): # not a TLD
            return root_info
        
        # Step 2: Query TLD Resolver
        tld_resolver = self.tld_resolvers.resolve(tld) # defined in DNS_TLD_resolver.py
        if not tld_resolver:
            return "NXDOMAIN"
        
        authoritative_file = self.tld_resolvers.find_tld_file(tld_resolver) # get the authoritative file

        # Step 3: Query Authoritative Resolver
        self.authoritative_resolvers = DNS_authoritative_resolver(authoritative_file)
        return self.authoritative_resolvers.resolve(domain)

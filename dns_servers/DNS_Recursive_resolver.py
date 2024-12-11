from pathlib import Path

# Importing the resolvers
from DNS_root import DNS_Root_resolver  # root resolver
from DNS_TLD_resolver import DNS_TLD_resolver  # tld resolver
from DNS_authoritative_resolver import DNS_Authoritative_resolver  # authoritative resolver
import sys

sys.path.append("DNS_Query/dns_construction/")
from dns_packet import dns_packet
from DNS_resolver import Resolver

class DNS_Recursive_resolver(Resolver):
    """
    Recursive DNS server that resolves domain names using local, ISP, and root server caches.
    """
    def __init__(self,  dns_query: dns_packet, root_file: Path = Path("root.cache"), tld_file: Path = Path("TLD.cache"), authoritative_file: Path = Path("authorative.cache")):
        """
        Initializes the recursive DNS server.
        #TODO Fix this docstring
        :param local_cache: Path to the local DNS cache file.
        :param isp_cache: Path to the ISP DNS cache file.
        :param root_cache: Path to the root DNS cache file.
        :param port: Port to communicate with DNS servers (default is 53).
        """
        self.dns_query = dns_query

        #print("Setting up recursive")
        self.root_resolver = DNS_Root_resolver(dns_query, root_file)
        self.tld_resolvers = None # this will be set in the resolve method
        self.authoritative_resolvers = None # this will be set in the resolve method  
        #print("Recursive set-up done")

    def resolve(self) -> str:
        """
        Resolves a domain name using recursive resolvers.

        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        domain = self.dns_query.q.qname.domain_name
        parts = domain.split('.')
        if len(parts) < 2:
            return "NXDOMAIN" # Enough parts of it needed
        

        tld = parts[-1]
        zone = f"{parts[-2]}.{tld}"

        # Step 1: Query Root Resolver
        root_response = self.root_resolver.resolve()
        if root_response == "NXDOMAIN":
            return "NXDOMAIN"

        if not hasattr(root_response, 'NS'):
            return root_response
        
        # Step 2: Query TLD Resolver
        self.tld_resolvers = DNS_TLD_resolver(self.dns_query, root_response)
        tld_response = self.tld_resolvers.resolve()
        
        if tld_response == "NXDOMAIN":
            return "NXDOMAIN"
        
        # Step 3: Query Authoritative Resolver
        self.authoritative_resolvers = DNS_Authoritative_resolver(self.dns_query, tld_response)
        return self.authoritative_resolvers.resolve()
    

def main():
    recursive_resolver = DNS_Recursive_resolver()
    print(recursive_resolver.resolve("Paola.ORG."))
    
if __name__ == "__main__":
    main()
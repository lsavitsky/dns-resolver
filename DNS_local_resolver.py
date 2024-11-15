"""
Refence: https://www.iana.org/domains/root/files    - for the root file
"""
from dnslib import DNSRecord, DNSError, QTYPE, RCODE, RR

# This is a simple DNS resolver that can resolve certain types of DNS queries.

class DNSLocalResolver(object):
    """
    This class is a simple DNS resolver that can resolve certain types of DNS queries.
    It is designed to be used with an object of the class.
    """
    
    
    
    
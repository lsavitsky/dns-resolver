import sys 

sys.path.append("dns_servers/DNS_Query/dns_construction/")
from DNS_Tunnel_enums import EncodingType
from dns_question_enum import QNAME, QTYPE, QCLASS
from dns_packet import dns_packet

sys.path.append("dns_servers/")
from DNS_local_resolver import DNS_Local_resolver

### The code is a controller that will be used to control the flow of the DNS resolution process.

def validate_encoding_type(encoding_type):
    """
    Validates the encoding type.

    :param encoding_type: The encoding type to validate.
    :return: True if the encoding type is valid, raises ValueError otherwise.
    """
    if encoding_type not in EncodingType.__members__:
        raise ValueError(f"Invalid encoding type: {encoding_type}. Must be one of {', '.join(EncodingType.__members__)}.")
    
    return encoding_type

def validate_record_type(record_type):
    """
    Validates the DNS record type.

    :param record_type: The DNS record type to validate.
    :return: True if the record type is valid, raises ValueError otherwise.
    """
    if not QTYPE.is_valid_name(record_type):
        raise ValueError(f"Invalid record type: {record_type}. Must be one of {', '.join(QTYPE.__members__)}.")
    
    return record_type

def validate_dns_name(dns_name):
    """
    Validates the DNS name format, including TLD check.

    :param dns_name: The DNS name to validate.
    :return: True if the DNS name is valid, raises ValueError otherwise.
    """
    valid_tlds = {"com", "net", "edu", "org", "gov", "mil", "int", "io", "co", "biz", "info", "xyz"}
    
    labels = dns_name.split(".")

    if len(labels) < 2:
        raise ValueError("DNS name must have at least two labels.")
    
    tld = labels[-1].lower()
    
    if tld not in valid_tlds:
        raise ValueError(f"Invalid TLD: {tld}. Must be one of {', '.join(valid_tlds)}.")
    
    return dns_name

def dns_resolution(dns_query_active: dns_packet) -> str:
    """ 
    \nResolves the DNS query.
    \nThis function raises an exception if the DNS query is invalid.
    
    :param dns_query_active: The DNS query to resolve.
    :return: The resolved DNS query.
    """
    return DNS_Local_resolver(dns_query_active).resolve()
    
    
def controller(qname: QNAME, qtype: QTYPE = QTYPE.A, qclass: QCLASS = QCLASS.IN, transation_id= None) -> dns_packet:
    """ 
    \nControls the flow of the DNS resolution process.
    
    :param qname: The DNS name to resolve.
    :param qtype: The DNS record type to resolve.
    :param qclass: The DNS class to resolve.
    :param transation_id: The transaction ID to resolve.
    :return: The resolved DNS query.
    """
    dns_query_active = dns_packet(qname, qtype, qclass, transation_id) #Active one made and encoded based on given user input
    dns_query_active.q.qname.domain_name = dns_query_active.q.qname.encode_tunnel(dns_query_active.q.qname.domain_name)
    return dns_query_active

def get_dns_query(dns_name: str, record_type: str, encoding_type: str) -> dns_packet:
    """
    \nResolves the DNS query based on the user input.
    
    :param dns_name: The DNS name to resolve.
    :param record_type: The DNS record type to resolve.
    :param encoding_type: The encoding type to resolve.
    :return: The resolved DNS query.
    """
    try:
        create_qname = QNAME(dns_name, EncodingType[encoding_type])
        create_qtype = QTYPE[record_type]
        create_qclass = QCLASS.IN
    except ValueError as e:
        raise ValueError(f"Error: {e} when resolving the DNS query.")
        
    return controller(create_qname, create_qtype, create_qclass)


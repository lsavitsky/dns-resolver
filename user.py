import sys 
import time
import csv
import os 

sys.path.append("dns_servers/DNS_Query/dns_construction/")
from DNS_Tunnel_enums import EncodingType
from dns_question_enum import QNAME, QTYPE, QCLASS
from dns_packet import dns_packet

sys.path.append("dns_servers/")
from DNS_local_resolver import DNS_Local_resolver


# print(sys.path)

# sys.path.append("validation/")
# import InvalidCacheLineError
# import InvalidRecordTypeError


def validate_encoding_type(encoding_type):
    """
    Validates the encoding type.

    :param encoding_type: The encoding type to validate.
    :return: True if the encoding type is valid, raises ValueError otherwise.
    """
    if encoding_type not in EncodingType.__members__:
        raise ValueError(f"Invalid encoding type: {encoding_type}. Must be one of {', '.join(EncodingType.__members__)}.")
    
    return True

def validate_record_type(record_type):
    """
    Validates the DNS record type.

    :param record_type: The DNS record type to validate.
    :return: True if the record type is valid, raises ValueError otherwise.
    """
    if not QTYPE.is_valid_name(record_type):
        raise ValueError(f"Invalid record type: {record_type}. Must be one of {', '.join(QTYPE.__members__)}.")
    
    return True

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
    
    return True

def dns_resolution(dns_query_active: dns_packet):
    
    resolution= DNS_Local_resolver(dns_query_active).resolve()
    
    
def controller(qname: QNAME, qtype: QTYPE = QTYPE.A, qclass: QCLASS = QCLASS.IN, transation_id= None):
    dns_query_active = dns_packet(qname, qtype, qclass, transation_id) #Active one made and encoded based on given user input
    dns_query_active.q.qname.domain_name = dns_query_active.q.qname.encode_tunnel(dns_query_active.q.qname.domain_name)
    return dns_query_active

def dataMain():
    try:
        print("\nWelcome to the DNS Query Tool!\n")

        # prompt for the DNS name
        dns_name = input("Enter the DNS name to query (e.g., example.com): ").strip()
        
        try:
            validate_dns_name(dns_name)
        except ValueError as e:
            print(f"Error: {e}")
            
        # prompt for the DNS record type
        record_type = input("Enter the DNS record type to query (e.g., A): ").strip().upper()
        
        try:
            validate_record_type(record_type)
        except ValueError as e:
            print(f"Error: {e}")
        
        # prompt for the encoding type
        encoding_type = input("Enter the encoding type (e.g., Base16): ").strip()
        try:
            validate_encoding_type(encoding_type)
        except ValueError as e:
            print(f"Error: {e}")
        
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        
    #print("QTYPE: ", QTYPE[record_type])

    dns_query_active= controller(QNAME(dns_name, EncodingType[encoding_type]), QTYPE[record_type] , QCLASS.IN)

    
def Tests(dns_name, record_type, encoding_type): 
    encodePacketStart=time.perf_counter() # For data Collection 
    dns_query_active= controller(QNAME(dns_name, EncodingType[encoding_type]), QTYPE[record_type] , QCLASS.IN)
    
    encodePacketEnd =time.perf_counter() # For data Collection
    
    dnsResStart=time.perf_counter()
    dns_resolution(dns_query_active)
    dnsResEnd=time.perf_counter()


    csv_file = "dns_timing_results.csv"
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        encode_duration = encodePacketEnd - encodePacketStart
        dns_resolution_duration = dnsResEnd - dnsResStart
        total_duration = dnsResEnd - encodePacketStart
        
    
        if file.tell() == 0: #IF needed write header
            writer.writerow([
                "domain", "record_type", "encoding_type",
                "encodePacketStart", "encodePacketEnd", "dnsResStart", "dnsResEnd", "encode_duration","dns_resolution_duration", "total_duration" ])
        
        writer.writerow([dns_name, record_type, encoding_type,
            encodePacketStart, encodePacketEnd, dnsResStart, dnsResEnd, encode_duration, dns_resolution_duration, total_duration])
        
def main_collect_tunneling_data():
    dns_name = "example.com"
    record_types = ['A', 'AAAA']
    encoding_types = EncodingType.__members__


    for _ in range(200):
        for record_type in record_types:
            for encoding_type in encoding_types:
                Tests(dns_name, record_type, encoding_type)

    

if __name__ == "__main__":
    # main()
    main_collect_tunneling_data()

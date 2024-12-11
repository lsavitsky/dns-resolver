
from dnslib import DNSRecord, QTYPE
from DNS_Tunnel_enums import EncodingType, DNS_Record_Type
"""
    Simple Driver testing
"""
message = "Red panda time!!!"

encoding =EncodingType.Base32 
record_type = DNS_Record_Type.TXT 

encoded_message = encoding.encode(message) # Alls the specific encoding on the msg
# Construction of DNS Query #
query_name = f"{encoded_message}.example.com"  # Replace with your domain

query = DNSRecord.question(query_name, getattr(QTYPE, record_type.value))
print(query)
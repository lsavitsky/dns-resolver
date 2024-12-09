from enum import Enum
from DNS_Tunnel_enums import EncodingType

class QTYPE(Enum):
    """
    Enum for DNS record types.
    """
    A = 1
    NS = 2
    CNAME = 5
    SOA = 6 
    PTR = 12
    MX = 15
    TXT =16
    AAAA = 28
    SRV = 33
    NULL = 10
    ANY = 255  # General 

    @classmethod
    def get_name(cls, value: int) -> str:
        """
        Get the name of a DNS record type from value.

        :param value: The numerical value of the DNS record type.
        :return: The name of the corresponding DNS record type.
        :raises ValueError: If the value does not match any record type.
        """
        for record in cls:
            if record.value == value:
                return record.name
        raise ValueError(f"Unknown DNS record value: {value}")
    @classmethod
    def get_value(cls, name: str) -> int:
        """
        Get the numerical value of a DNS record type by its name.

        :param name: The name of the DNS record type.
        :return: The numerical value of the corresponding DNS record type.
        :raises ValueError: If the name does not match any record type.
        """
        try:
            return cls[name].value
        except KeyError:
            raise ValueError(f"Unknown DNS record type: {name}")
    @classmethod  
    def is_valid_name(cls, name: str) -> bool:
        """
        Check if the given name is a valid DNS record type.

        :param name: The name to validate.
        :return: True if the name is a valid DNS record type, False otherwise.
        """
        return name in cls.__members__
    @classmethod
    def is_valid_value(cls, value: int) -> bool:
        """
        Check if the given value is a valid DNS record type.

        :param value: The numerical value to validate.
        :return: True if the value is a valid DNS record type, False otherwise.
        """
        return value in (record.value for record in cls)

    
### Answer Section ###
#No clue what this one is for but I assume use of IN
class QCLASS(Enum):
    IN = 1         # Internet
    CS = 2         # CSNET (obsolete)
    CH = 3         # Chaos
    HESIOD = 4     # Hesiod
    NONE = 254     # None
    ANY = 255      # Any class
    
    @classmethod
    def construct_class_bits (cls, class_: "CLASS" ) -> int:
        """
        Generate the RCODE bits for the DNS header.

        :param rcode: RCODE - RCODE enum value selection.
        :return: Integer representation of the OPCODE bit at position  0-3.
        """
        return class_.value << 0 # handle bitfield at the 0-3
    
class QNAME():
    """
    QNAME handling of the domain name
    """
    def __init__(self, domain_name: str, encoding: EncodingType = EncodingType.Base32):
        """
        Initialize the QNAME with a domain name.

        :param domain_name: The domain name (e.g., "www.example.com").
        :param encoding: The encoding type to use for tunneling.

        """
        self.domain_name = domain_name
        self.encoding = encoding
        
    def encode(self) -> bytes:
        """
        BASIC 
        Encode the domain name into the DNS label format.
        :return: The encoded domain name as bytes.
        """
        labels = self.domain_name.split(".") #www. example .com split up
        encoded = b"".join(len(label).to_bytes(1, "big") + label.encode() for label in labels) #uses encoding properly with the other file
        return encoded + b"\x00"  # End with a null byte for consistency and due to format
    
    
    def decode(cls, encoded_qname: bytes) -> str:
        """
        ONLINE... #TODO Change this temp thing
        Decode a DNS label format QNAME back into a human-readable domain name.

        :param encoded_qname: The encoded QNAME in DNS label format.
        :return: The decoded domain name as a string.
        """
        labels = []
        i = 0
        while i < len(encoded_qname):
            length = encoded_qname[i]
            if length == 0:  # End of QNAME
                break
            i += 1
            labels.append(encoded_qname[i:i + length].decode())
            i += length
        return ".".join(labels)
    
    def encode_tunnel(self, data: str ) -> bytes:
        """
        encode_tunnel - encodes with the given way of encoding
        :param data: the middle of the domain section for example: example in example.com
        #TODO - Fix these docstrings...
        :param extension: extension like .com
        :return: The encoded data as bytes.
        """
        
        domain_list = data.split('.')
        word, extension = domain_list[0], domain_list[1]
        # encoded_data = self.encoding.encode(word) #using given
        tunneling_qname = f"{word}.{extension}" #passed encoded .com
        return self.encoding.encode(tunneling_qname)
    
    def decode_tunnel(self, qname:bytes )-> str:
        """
        :param qname: The encoded QNAME in DNS label format.
        :return: The decoded data as a string.
        """
        #domain_name = self.decode(qname) #initial decode
        #encoded_data, _ = domain_name.split(".", 1) #split the end off .com
        return self.encoding.decode(qname) # decode with alt of the encode
    
    
class q_construction:
    """
    Constructs the binary representation of the DNS Question Section, this will be used with the other sections to create the payload
    including QNAME, QTYPE, and QCLASS.
    """

    def __init__(self, qname: QNAME, qtype: QTYPE = QTYPE.A, qclass: QCLASS = QCLASS.IN):
        """
        Initialize the Question Section with QNAME, QTYPE, and QCLASS.

        :param qname: An instance of QNAME for domain name handling.
        :param qtype: Query type (e.g., A, AAAA, MX).
        :param qclass: Query class (e.g., IN).
        """
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    def construct(self) -> bytes:
        """
        Construct the binary representation of the Question Section.

        :return: The serialized Question Section as bytes.
        """
        # Encode QNAME into bytes
        qname_bytes = self.qname.encode()
        # Convert QTYPE and QCLASS to their binary representations
        qtype_bytes = self.qtype.value.to_bytes(2, "big")
        qclass_bytes = self.qclass.value.to_bytes(2, "big")
        # Combine all parts into the full Question Section
        return qname_bytes + qtype_bytes + qclass_bytes



# Example Usage for Tunneling
if __name__ == "__main__":
    # Original data to tunnel
    data = "secret_data"

    # Subdomain for the DNS query
    subdomain = "example.com"

    # Choose encoding type
    encoding = EncodingType.Base32

    # Create QNAME instance
    qname = QNAME("", encoding)

    # Encode data into QNAME
    encoded_qname = qname.encode_tunnel(data, subdomain)
    print(f"Encoded Tunneling QNAME (Base32): {encoded_qname()}")

    # Decode tunneled data from QNAME
    decoded_data = qname.decode_tunnel(encoded_qname)
    print(f"Decoded Tunneling Data: {decoded_data}")
    

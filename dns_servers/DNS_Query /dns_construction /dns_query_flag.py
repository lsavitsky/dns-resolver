from enum import Enum, IntFlag

#### ENUMS FOR 16 bit FLAGS#####
        

class OPCODE(Enum):
    """
    OPCODE: Operation code
    """
    QUERY = 0 
    IQUERY = 1
    STATUS = 2
    NOTIFY = 4
    UPDATE = 5 # Dynamic DNS updates
    
    @classmethod
    def construct_opcode_bits (cls, opcode: "OPCODE" ) -> int:
        """
        Generate the OPCODE bits for the DNS header.

        :param opcode: OPCODE - OPCODE enum value selection.
        :return: Integer representation of the OPCODE bit at position  11-14.
        """
        return opcode.value <<11 # handle bitfield at the 11-14 
class RCODE(Enum):
    """
    RCODE: Response code
    """
    NOERROR = 0
    FORMERR = 1
    SERVFAIL = 2
    NXDOMAIN = 3
    NOTIMP = 4
    REFUSED = 5
    YXDOMAIN = 6
    YXRRSET = 7
    NXRRSET = 8
    NOTAUTH = 9
    NOTZONE = 10
    BADVERS = 16
    # Other possible codes used that were discovered
    BADKEY = 17     # Bad key (DNSSEC)
    BADTIME = 18    # Bad timestamp (DNSSEC)
    BADMODE = 19    # Bad mode
    BADNAME = 20    # Bad name
    BADALG = 21     # Bad algorithm
    BADTRUNC = 22   # Bad truncation
    
    @classmethod
    def construct_rcode_bits (cls, rcode: "RCODE" ) -> int:
        """
        Generate the RCODE bits for the DNS header.

        :param rcode: RCODE - RCODE enum value selection.
        :return: Integer representation of the OPCODE bit at position  0-3.
        """
        return rcode.value << 0 # handle bitfield at the 0-3


class QR(Enum):
    """
    QR: Query or Response 
    """
    QUERY = 0
    RESPONSE = 1
    
    @staticmethod
    def construct_qr_bits(qr: "QR") -> int:
        """
        Generate the QR bits for the DNS header.

        :param qr: QR - QR enum value (QUERY or RESPONSE).
        :return: Integer representation of the QR bit at position 15.
        """
        return qr.value << 15 # leftmost bit (15th bit) represents QR in the DNS flags field
    @staticmethod
    def print_bin(qr: "QR") -> None:
        """
        For print bin testing of the bits
        :param qr: QR - QR enum value (QUERY or RESPONSE).

        """
        qr_bits = qr.construct_qr_bits(qr)
        print(f"QR {qr.name} ({qr.value}) in binary: {bin(qr_bits)}")
        
class DNSFlags(IntFlag):
    QR = 1 << 15   # Query (0) or Response (1)
    AA = 1 << 10   # Authoritative Answer
    TC = 1 << 9    # Truncated
    RD = 1 << 8    # Recursion Desired
    RA = 1 << 7    # Recursion Available
    AD = 1 << 5    # CONFUSION
    CD = 1 << 4    # Discabled checking
    # Reserved and RCODE (bits 12-15) are managed separately
    
    @classmethod
    def construct_flag_bits(cls, rd:bool=True, ra:bool=False, aa:bool=False, ad:bool=False, cd:bool=False) -> int:
        """
        Construction for a section of 16-bit DNS header flags field.
        Default values listed to the right of each discription.
        
        # :param qr: DNSFlag - Query or Response (QR flag) with default of the QUERY enum 
        :param rd: DNSFlag - Recursion Desired (RD flag). True
        :param ra: DNSFlag -  Recursion Available (RA flag). False
        :param aa: DNSFlag - Authoritative Answer (AA flag). False
        :param ad: DNSFlag - Authenticated Data (AD flag). False
        :param cd: DNSFlag - Checking Disabled (CD flag). False
        :return: Integer representation of the DNS header flags.
        """
        # Initialize flags
        flags = 0 # initial

        conditions = {
            cls.RD: rd,
            cls.RA: ra,
            cls.AA: aa,
            cls.AD: ad,
            cls.CD: cd,
         }
        for flag, condition in conditions.items():
            if condition: # If the glag is included
                flags |= flag # Properly handled -  combines the existing value of flags with the value of flag
        
        return flags
    # @staticmethod
    # def print_flags():
    #     print(f"DNS Flags: {bin(dns_query.FLAGS)}")
    

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
class CLASS(Enum):
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
    
    
    
    
"""
    Container for the DNS query and enum types
"""
class dns_query_flag:
    """
        For the inital 16 bits of the flags
    """
    QR = QR.QUERY
    OPCODE = OPCODE.QUERY
    QTYPE = QTYPE.A
    RCODE = RCODE.NOERROR
    FLAGS = DNSFlags(0)

    @staticmethod
    def construct_bits(qr: "QR" =QR.QUERY, opcode: "OPCODE" = OPCODE.QUERY, rcode: "RCODE" = RCODE.NOERROR, rd:bool=True, ra:bool=False, aa:bool=False, ad:bool=False, cd:bool=False) -> int:
        """
        Construction for a section of 16-bit DNS header flags field.
        Default values listed to the right of each discription.
        
        :param qr: QR enum value - Query or Response (QR flag) with default of the QUERY enum 
        :param opcode: OPCODE enum value type.
        :param rcode: RCODE enum value type.
        :param rd: DNSFlag - Recursion Desired (RD flag). True
        :param ra: DNSFlag -  Recursion Available (RA flag). False
        :param aa: DNSFlag - Authoritative Answer (AA flag). False
        :param ad: DNSFlag - Authenticated Data (AD flag). False
        :param cd: DNSFlag - Checking Disabled (CD flag). False
        """
        flags= 0 #bits of 16 all will be 0 at first.. hopefully
        # CALL OTHER CLASSES WITH THE CONSTRUCTIONS 
        flags |= QR.construct_qr_bits(qr)
        print(bin(flags))
        flags |= OPCODE.construct_opcode_bits(opcode)
        print(bin(flags))
        flags |= DNSFlags.construct_flag_bits(rd=rd, ra=ra, aa=aa, ad=ad, cd=cd)
        print(bin(flags))
        flags |= RCODE.construct_rcode_bits(rcode)
        print(bin(flags))

        return flags

    
    ## FOR QR BIT PRINT CHECKING ##
    

    
def test_qr():
    print("************* QR *************")
    for qr in QR:
        print(f"{qr.name} IS:")
        QR.print_bin(qr)
    
    print("************* QR *************")

def test_opcode():
    print("************* OPCODE *************")
    for opcode in OPCODE:
        opcode_bits = OPCODE.construct_opcode_bits(opcode)
        print(f"{opcode.name} ({opcode.value}) in binary: {bin(opcode_bits)}")
    print("************* OPCODE *************\n")


def test_rcode():
    print("************* RCODE *************")
    for rcode in RCODE:
        rcode_bits = RCODE.construct_rcode_bits(rcode)
        print(f"{rcode.name} ({rcode.value}) in binary: {bin(rcode_bits)}")
    print("************* RCODE *************\n")

def test_dns_flags():
    print("************* DNS FLAGS *************")
    scenarios = [
        {"rd": True, "ra": False, "desc": "RD=True, RA=False"},
        {"rd": True, "ra": True, "desc": "RD=True, RA=True"},
        {"rd": False, "ra": False, "desc": "RD=False, RA=False"},
    ]
    for scenario in scenarios:
        flags = DNSFlags.construct_flag_bits(
            rd=scenario["rd"], ra=scenario["ra"]
        )
        print(f"{scenario['desc']} in binary: {bin(flags)}")
    print("************* DNS FLAGS *************\n")

def test_overall():
    
    print("************* DEFAULT FLAGS *************")
    default_header = dns_query_flag.construct_bits()
    print(f"Constructed Flags (binary): {bin(default_header)}")
    print(f"Constructed Flags (hex): {hex(default_header)}")
    print("************* END DEFAULT FLAGS *************")
    all_true = dns_query_flag.construct_bits(
        qr=QR.RESPONSE,
        opcode=OPCODE.UPDATE, 
        rcode=RCODE.REFUSED,  
        rd=True,
        ra=True,
        aa=True,
        ad=True,
        cd=True 
    )
    print("************* TRUE ALL FLAGS *************")
    print(f"Constructed Flags (binary): {bin(all_true)}")
    print(f"Constructed Flags (hex): {hex(all_true)}")
    print("************* TRUE ALL FLAGS *************")

    
def run_tests():
    test_qr()
    test_opcode()
    test_rcode()
    test_dns_flags()
    test_overall()
    
             
if __name__ == "__main__":
    run_tests()
    # header_bits = dns_query_flag.construct_bits(
    #     qr=QR.QUERY,
    #     opcode=OPCODE.QUERY,
    #     rcode=RCODE.NOERROR,
    #     rd=True,
    #     ra=False,
    #     aa=False,
    #     ad=False,
    #     cd=False
    # )
     
    # print(f"Constructed DNS header flags (binary): {bin(header_bits)}")
    # print(f"Constructed DNS header flags (hex): {hex(header_bits)}")
    
import random

class dns_transaction_ID: 
    @staticmethod
    def random_ID() ->int:
        """
        Random 16-bit transaction ID for first 16-bits 
        :return: 16-bit integer
        """
        return random.getrandbits(16)


class dns_counters:
    """
    Counts (48 bits):
        QDCOUNT (16 bits): Number of entries in the Question section.
        ANCOUNT (16 bits): Number of resource records in the Answer section.
        NSCOUNT (16 bits): Number of name server resource records in the Authority section.
        ARCOUNT (16 bits): Number of resource records in the Additional section.    
    """
    def __init__(self, qdcount=1, ancount=0, nscount=0, arcount=0):
        """
            Counters for each step
        """
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount


    def bytes_format(self)-> bytes:
        """
        Each of them take up 16-bits in placement. 
        All together will be 6 bytes (according to online)
        :return: #TODO
        """
        
        # Put them together uses byteof_ made method
        counters = [self.byteof_("qdcount"), self.byteof_("ancount"), self.byteof_("nscount"), self.byteof_("arcount")]
        return b"".join(counters)
    
    
    def byteof_(self, counter_name_type : str) -> bytes:
        """
        byteof_  gives the bytes for just the one counter desired
        :return: #TODO
        :raises ValueError: If the counter_name_type is invalid.

        """
        if not hasattr(self, counter_name_type): #attempt to verify the attribute if not err
            raise ValueError(f"Invalid counter name: {counter_name_type}")

        value = getattr(self, counter_name_type)
        return value.to_bytes(2, "big") # Will be a 2 bytes aka 16 bits 
    
    
    def __repr__(self):
        """
        Taken from online mostly...
        #TODO 
        """
        return (
            f"<dns_counters(QDCOUNT={self.qdcount}, ANCOUNT={self.ancount}, "
            f"NSCOUNT={self.nscount}, ARCOUNT={self.arcount})>"
        )




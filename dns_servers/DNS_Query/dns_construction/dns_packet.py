from dns_question_enum import *
from dns_header_construction import *

class dns_packet:
    """
    Constructs a full DNS packet by combining the header and question section.
    """

    def __init__(self, qname: QNAME, qtype: QTYPE = QTYPE.A, qclass: QCLASS = QCLASS.IN, transation_id= None, flags=0, counts =None):
        """
        Qname must be QNAME("", encoding) where "" is the domain name and encoding is the encoding type
        """
        self.q=q_construction(qname, qtype, qclass)
        self.header= dns_header(transation_id, flags, counts)
        
    def construct_packet(self) -> bytes:
        """
        Combine the header and question section into a full DNS packet.

        :return: The full DNS packet as bytes.
        """
        # Serialize the header and question section
        header_bytes = self.header.byte_format_construction()
        question_bytes = self.q.construct()
        return header_bytes + question_bytes
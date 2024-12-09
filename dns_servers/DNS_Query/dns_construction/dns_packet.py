from dns_question_enum import q_construction
from dns_header_construction import dns_header
class dns_packet:
    """
    Constructs a full DNS packet by combining the header and question section.
    """
    def __init__():
        q=q_construction()
        header= dns_header()
        
    def construct_packet(self) -> bytes:
        """
        Combine the header and question section into a full DNS packet.

        :return: The full DNS packet as bytes.
        """
        # Serialize the header and question section
        header_bytes = self.header.byte_format_construction()
        question_bytes = self.question.construct()
        return header_bytes + question_bytes
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
    def __init__(self, qdcount=1, ancount=0, nscount=0, arcount=0):
        """
            Counters for each step
        """
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount


    def bytes_format(self)-> bytes:
        pass






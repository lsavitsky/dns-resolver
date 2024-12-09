# from enum import Enum

# class QTYPE(Enum):
#     """
#     Enum for DNS record types.
#     """
#     A = 1
#     NS = 2
#     CNAME = 5
#     SOA = 6 
#     PTR = 12
#     MX = 15
#     TXT =16
#     AAAA = 28
#     SRV = 33
#     NULL = 10
#     ANY = 255  # General 


#     def get_name(cls, value: int) -> str:
#         """
#         Get the name of a DNS record type from value.

#         :param value: The numerical value of the DNS record type.
#         :return: The name of the corresponding DNS record type.
#         :raises ValueError: If the value does not match any record type.
#         """
#         for record in cls:
#             if record.value == value:
#                 return record.name
#         raise ValueError(f"Unknown DNS record value: {value}")
 
#     def get_value(cls, name: str) -> int:
#         """
#         Get the numerical value of a DNS record type by its name.

#         :param name: The name of the DNS record type.
#         :return: The numerical value of the corresponding DNS record type.
#         :raises ValueError: If the name does not match any record type.
#         """
#         try:
#             return cls[name].value
#         except KeyError:
#             raise ValueError(f"Unknown DNS record type: {name}")
        
#     def is_valid_name(cls, name: str) -> bool:
#         """
#         Check if the given name is a valid DNS record type.

#         :param name: The name to validate.
#         :return: True if the name is a valid DNS record type, False otherwise.
#         """
#         return name in cls.__members__
#     def is_valid_value(cls, value: int) -> bool:
#         """
#         Check if the given value is a valid DNS record type.

#         :param value: The numerical value to validate.
#         :return: True if the value is a valid DNS record type, False otherwise.
#         """
#         return value in (record.value for record in cls)
    
    
# class QCLASS
from enum import Enum
import base64
import binascii
import base91  


class DNS_Record_Type(Enum):
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
        
    def is_valid_name(cls, name: str) -> bool:
        """
        Check if the given name is a valid DNS record type.

        :param name: The name to validate.
        :return: True if the name is a valid DNS record type, False otherwise.
        """
        return name in cls.__members__
    def is_valid_value(cls, value: int) -> bool:
        """
        Check if the given value is a valid DNS record type.

        :param value: The numerical value to validate.
        :return: True if the value is a valid DNS record type, False otherwise.
        """
        return value in (record.value for record in cls)
    
    
class EncodingType(Enum):
    """
    Enum for encoding types with associated methods for conversion.
    """
    Base16 = "Base16"
    Base32 = "Base32"
    Base64 = "Base64"
    Base85 = "Base85"
    Base91 = "Base91"
    Binary = "Binary"
    Hexadecimal ="Hexadecimal"
    NetBios = "NetBios"
    #XOR= "XOR"
    DecimalEncoding = "DecimalEncoding"
    ROT13 = "ROT13" # Simple Cipher
    URL = "URL"
    ALL = "ALL"
    
    def encode(self, message:str) -> str:
        """
            Encode data based on the data ad type
        """
        print("ENCODE: ", message.encode())
        print("*")
        if self == EncodingType.Base16:
            return base64.b16encode(message.encode()).decode()
        elif self == EncodingType.Base32:
            return base64.b32encode(message.encode()).decode()
        elif self == EncodingType.Base64:
            return base64.b64encode(message.encode()).decode()
        elif self == EncodingType.Base85:
            return base64.b85encode(message.encode()).decode()
        elif self == EncodingType.Base91:
            return base91.encode(message.encode())
        elif self == EncodingType.URL:
            import urllib.parse # REC
            return urllib.parse.quote(message)
        elif self == EncodingType.Hexadecimal:
            return binascii.hexlify(message.encode()).decode()
        elif self == EncodingType.NetBios:
            return message
        elif self == EncodingType.ROT13:
            return message.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                    "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"))
        elif self == EncodingType.DecimalEncoding:
            return '.'.join(str(ord(c)) for c in message)
        # elif self == EncodingType.XOR:
        #     key= b"key"
        #     return ''.join(chr(ord(c) ^ key[i % len(key)]) for i, c in enumerate(message))
        elif self == EncodingType.Binary:
            return ' '.join(format(ord(c), '08b') for c in message)
        elif  self == EncodingType.ALL: # Run at your own risk...
            # Sequentially encode using all encoding types except ALL once...
            result = message
            for encoding in EncodingType: #all encoding types
                if encoding != EncodingType.ALL:
                    result = encoding.encode(result)
            return result 
        else:
            print("How did you manage to forget to add it to the encode function..??")
            raise ValueError(f"Unsupported encoding type: {self.value}")
                    
    def decode(self, encoded_message:str) -> str:
        """
            Decode data based on the data ad type
        """
        if self == EncodingType.Base16:
            return base64.b16decode(encoded_message).decode()
        elif self == EncodingType.Base32:
            return base64.b32decode(encoded_message).decode()
        elif self == EncodingType.Base64:
            return base64.b64decode(encoded_message).decode()
        elif self == EncodingType.Base85:
            return base64.b85decode(encoded_message).decode()
        elif self == EncodingType.Base91:
            return str(base91.decode(encoded_message), 'utf-8') #byteArray
        elif self == EncodingType.URL:
            import urllib.parse # REC
            return urllib.parse.unquote(encoded_message)
        elif self == EncodingType.Hexadecimal:
            return binascii.unhexlify(encoded_message).decode()
        elif self == EncodingType.NetBios:
            return encoded_message                      #TODO
        elif self == EncodingType.ROT13:
            return encoded_message.translate(str.maketrans(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
            ))
        elif self == EncodingType.DecimalEncoding:
            return ''.join(chr(int(num)) for num in encoded_message.split('.'))
        # elif self == EncodingType.XOR:
        #     key= b"key"
        #     return ''.join(chr(ord(c) ^ key[i % len(key)]) for i, c in enumerate(encoded_message))
        elif self == EncodingType.Binary:
            return ''.join(chr(int(byte, 2)) for byte in encoded_message.split(' '))
        elif  self == EncodingType.ALL: # Run at your own risk...
            # Sequentially encode using all encoding types except ALL once...
            result = encoded_message
            for encoding in reversed(EncodingType): #all encoding types
                if encoding != EncodingType.ALL:
                    result = encoding.decode(result)
            return result 
        else:
            print("How did you manage to forget to add it to the decode function..??")
            raise ValueError(f"Unsupported encoding type: {self.value}")
                  
    
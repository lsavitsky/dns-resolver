from enum import Enum
import base64
import binascii
import base91  


class DNS_Record_Type(Enum):
    """
    Enum for DNS record types.
    """
    NULL = "NULL"
    TXT = "TXT"
    A = "A"
    AAAA = "AAAA"
    MX = "MX"
    
class EncodingType(Enum):
    """
    Enum for encoding types with associated methods for conversion.
    """
    Base16 = "Base16"
    Base32 = "Base32"
    Base64 = "Base64"
    Base85 = "Base85"
    Base91 = "Base91"
    Hexadecimal ="Hexadecimal"
    NetBios = "NetBios"
    XOR= "XOR"
    DecimalEncoding = "DecimalEncoding"
    ROT13 = "ROT13" # Simple Cipher
    URL = "URL"
    ALL = "ALL"
    
    def encode(self, message:str) -> str:
        """
            Encode data based on the data ad type
        """
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
        elif self == EncodingType.URLEncoding:
            import urllib.parse
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
        elif self == EncodingType.XOR:
            key= b"key"
            return ''.join(chr(ord(c) ^ key[i % len(key)]) for i, c in enumerate(message))
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
                  
    
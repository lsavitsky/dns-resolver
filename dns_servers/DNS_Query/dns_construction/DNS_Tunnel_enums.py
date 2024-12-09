from enum import Enum
import base64
import binascii
import base91  


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
    
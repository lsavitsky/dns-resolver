import unittest
from DNS_Tunnel_enums import EncodingType, DNS_Record_Type


class TestDNSRecordType(unittest.TestCase):
    def test_record_types(self):
        """
        Test that all DNS record types exist and their values are correct.
        """
        expected_record_types = {
            "NULL": "NULL",
            "TXT": "TXT",
            "A": "A",
            "AAAA": "AAAA",
            "MX": "MX"
        }
        for record_name, record_value in expected_record_types.items():
            with self.subTest(record_name=record_name):
                self.assertEqual(DNS_Record_Type[record_name].value, record_value)
                
                
#### ENCODING TESTING ####

class TestEncodingType(unittest.TestCase):
    def setUp(self):
        """
        Set up common test data for EncodingType tests.
        """
        self.test_messages = ["redpanda"] # HelloWorld]

    def test_encoding_types(self):
        """
        Test each encoding type except ALL for correctness with multiple messages.
        """
        expected_encodings = {
            # "HelloWorld": {
            #     EncodingType.Base16: "48656C6C6F576F726C64",
            #     EncodingType.Base32: "JBSWY3DPEB3W64TMMQ======",
            #     EncodingType.Base64: "SGVsbG9Xb3JsZA==",
            #     EncodingType.Base85: "NM&qnZ3f!r9F~<jS",
            #     EncodingType.Base91: "^/5=O<6`Io5#",
            #     EncodingType.Hexadecimal: "48656c6c6f576f726c64",
            #     EncodingType.DecimalEncoding: "72.101.108.108.111.87.111.114.108.100",
            #     EncodingType.ROT13: "UryybJbeyq",
            #     EncodingType.URL: "HelloWorld",
            # },
            "redpanda": {
                EncodingType.Base16: "72656470616E6461",
                EncodingType.Base32: "OJSWI4DBNZSGC===",
                EncodingType.Base64: "cmVkcGFuZGE=",
                EncodingType.Base85: "a%E(2VQyq$",
                EncodingType.Base91: "dP;Iw)_YLR",
                EncodingType.Hexadecimal: "72656470616e6461",
                EncodingType.DecimalEncoding: "114.101.100.112.97.110.100.97",
                EncodingType.ROT13: "erqcnaqn",
                EncodingType.URL: "redpanda",
            }
        }

        for message in self.test_messages:
            for encoding, expected in expected_encodings[message].items():
                with self.subTest(message=message, encoding=encoding):
                    encoded_message = encoding.encode(message)
                    self.assertEqual(encoded_message, expected)
 

## If desired could implement an XOR
    # def test_xor_encoding(self):
    #     """
    #     Test XOR encoding with multiple messages.
    #     """
    #     key = b"key"
    #     for message in self.test_messages:
    #         expected_xor_result = ''.join(
    #             chr(ord(c) ^ key[i % len(key)]) for i, c in enumerate(message)
    #         )
    #         with self.subTest(message=message):
    #             encoded_message = EncodingType.XOR.encode(message)
    #             self.assertEqual(encoded_message, expected_xor_result)

    def test_all_encoding(self):
        """
        Test ALL encoding to ensure it processes the message through all encodings sequentially.
        """
        for message in self.test_messages:
            result = message
            for encoding in EncodingType:
                if encoding != EncodingType.ALL:
                    result = encoding.encode(result)

            with self.subTest(message=message):
                all_encoded_message = EncodingType.ALL.encode(message)
                self.assertEqual(all_encoded_message, result)
                   


class TestEncodingTypeRoundTrip(unittest.TestCase):
    def setUp(self):
        """
        Set up common test data for EncodingType tests.
        """
        self.test_message = "redpanda"

    def test_round_trip_encoding_decoding(self):
        """
        Test that encoding followed by decoding returns the original message.
        """
        encoding_types = [EncodingType.Base32, EncodingType.Base64, EncodingType.Base85, EncodingType.Base91]
        
        for encoding in encoding_types:
            with self.subTest(encoding=encoding):
                # Encode the message
                encoded_message = encoding.encode(self.test_message)
                
                # Decode the encoded message
                decoded_message = encoding.decode(encoded_message)
                
                # Verify the round-trip result
                self.assertEqual(decoded_message, self.test_message, 
                                 f"Failed for {encoding}: Encoded={encoded_message}, Decoded={decoded_message}")



### DECODING TESTS ###
class test_decoding(unittest.TestCase):
    def setUp(self):
        """
        Set up common test data for DecodingType tests.
        """
        self.test_messages = ["redpanda"]
    def test_decoding_types(self):
        """
        Test each decoding type except ALL for correctness with multiple messages.
        """
        expected_encodings = {
            "redpanda": {
                EncodingType.Base16: "72656470616E6461",
                EncodingType.Base32: "OJSWI4DBNZSGC===",
                EncodingType.Base64: "cmVkcGFuZGE=",
                EncodingType.Base85: "a%E(2VQyq$",
                EncodingType.Base91: "dP;Iw)_YLR",
                EncodingType.Hexadecimal: "72656470616e6461",
                EncodingType.DecimalEncoding: "114.101.100.112.97.110.100.97",
                EncodingType.ROT13: "erqcnaqn",
                EncodingType.URL: "redpanda",
            }
        }

        for original_message, encodings in expected_encodings.items():
            for encoding, encoded_message in encodings.items():
                with self.subTest(original_message=original_message, encoding=encoding):
                    decoded_message = encoding.decode(encoded_message)
                    self.assertEqual(decoded_message, original_message)

    def test_all_decoding(self):
        """
        Test ALL decoding to ensure it reverses the ALL encoding correctly.
        """
        for message in self.test_messages:
            encoded_message = EncodingType.ALL.encode(message)
            decoded_message = EncodingType.ALL.decode(encoded_message)
            with self.subTest(message=message):
                self.assertEqual(decoded_message, message)
                
                
if __name__ == "__main__":
    unittest.main()
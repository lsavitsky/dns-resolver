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



# Now Test Encoding


class TestEncodingType(unittest.TestCase):
    def setUp(self):
        """
        Set up common test data for EncodingType tests.
        """
        self.test_message = "HelloWorld"

    def test_encoding_types(self):
        """
        Test each encoding type except ALL for correctness.
        """
        expected_encodings = {
            EncodingType.Base16: "48656C6C6F576F726C64",  # Base16
            EncodingType.Base32: "JBSWY3DPEB3W64TMMQ======",  # Base32
            EncodingType.Base64: "SGVsbG9Xb3JsZA==",  # Base64
            EncodingType.Base85: "NM&qnZ3f!r9F~<jS",  # Base85
            EncodingType.Base91: "^/5=O<6`Io5#",  # Base91 (may vary depending on implementation)
            EncodingType.Hexadecimal: "48656c6c6f576f726c64",  # Hexadecimal
            EncodingType.DecimalEncoding: "72.101.108.108.111.87.111.114.108.100",  # Decimal Encoding
            EncodingType.ROT13: "UryybJbeyq",  # ROT13
            EncodingType.URL: "HelloWorld",  # URL (unchanged as it doesn't contain special chars)
        }
        
      
        for encoding, expected in expected_encodings.items():
            with self.subTest(encoding=encoding):
                encoded_message = encoding.encode(self.test_message)
                self.assertEqual(encoded_message, expected)

    def test_xor_encoding(self):
        """
        Test XOR encoding.
        """
        key = b"key"
        expected_xor_result = ''.join(
            chr(ord(c) ^ key[i % len(key)]) for i, c in enumerate(self.test_message)
        )
        encoded_message = EncodingType.XOR.encode(self.test_message)
        self.assertEqual(encoded_message, expected_xor_result)

    def test_all_encoding(self):
        """
        Test ALL encoding to ensure it processes the message through all encodings sequentially.
        """
        result = self.test_message
        for encoding in EncodingType:
            if encoding != EncodingType.ALL:
                result = encoding.encode(result)

        all_encoded_message = EncodingType.ALL.encode(self.test_message)
        self.assertEqual(all_encoded_message, result)
if __name__ == "__main__":
    unittest.main()
import sys 

sys.path.append("dns_servers/DNS_Query/dns_construction/")
import DNS_Tunnel_enums
import dns_question_enum

def validate_encoding_type(encoding_type):
    """
    Validates the encoding type.

    :param encoding_type: The encoding type to validate.
    :return: True if the encoding type is valid, raises ValueError otherwise.
    """
    if encoding_type not in DNS_Tunnel_enums.EncodingType.__members__:
        raise ValueError(f"Invalid encoding type: {encoding_type}. Must be one of {', '.join(DNS_Tunnel_enums.EncodingType.__members__)}.")
    
    return True

def validate_record_type(record_type):
    """
    Validates the DNS record type.

    :param record_type: The DNS record type to validate.
    :return: True if the record type is valid, raises ValueError otherwise.
    """
    if not dns_question_enum.QTYPE.is_valid_name(record_type):
        raise ValueError(f"Invalid record type: {record_type}. Must be one of {', '.join(dns_question_enum.QTYPE.__members__)}.")
    
    return True

def validate_dns_name(dns_name):
    """
    Validates the DNS name format, including TLD check.

    :param dns_name: The DNS name to validate.
    :return: True if the DNS name is valid, raises ValueError otherwise.
    """
    valid_tlds = {"com", "net", "edu", "org", "gov", "mil", "int", "io", "co", "biz", "info", "xyz"}
    
    labels = dns_name.split(".")

    if len(labels) < 2:
        raise ValueError("DNS name must have at least two labels.")
    
    tld = labels[-1].lower()
    
    if tld not in valid_tlds:
        raise ValueError(f"Invalid TLD: {tld}. Must be one of {', '.join(valid_tlds)}.")
    
    return True


def main():
    try:
        print("\nWelcome to the DNS Query Tool!\n")

        # prompt for the DNS name
        dns_name = input("Enter the DNS name to query (e.g., example.com): ").strip()
        
        try:
            validate_dns_name(dns_name)
        except ValueError as e:
            print(f"Error: {e}")
            
        # prompt for the DNS record type
        record_type = input("Enter the DNS record type to query (e.g., A): ").strip().upper()
        
        try:
            validate_record_type(record_type)
        except ValueError as e:
            print(f"Error: {e}")
        
        # prompt for the encoding type
        encoding_type = input("Enter the encoding type (e.g., ASCII): ").strip()
        try:
            validate_encoding_type(encoding_type)
        except ValueError as e:
            print(f"Error: {e}")
        
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")

if __name__ == "__main__":
    main()

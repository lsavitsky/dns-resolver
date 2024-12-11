# This file contains a simple user interface for the DNS Query Tool.
from controller import *

def get_dns_name():
    """
    \nPrompts the user to enter a DNS name.
    
    :return: The DNS name entered by the user.
    """
    dns_name = input("Enter the DNS name to query (e.g., example.com): ").strip()
    valid = False
    
    while not valid:
        try:
            valid = validate_dns_name(dns_name)
        except ValueError as e:
            print(f"Error: {e}")
            dns_name = input("Enter the DNS name to query (e.g., example.com): ").strip()
    
    return valid

def get_record_type():
    """
    \nPrompts the user to enter a record type.
    
    :return: The record type entered by the user.
    """
    record_type = input("Enter the record type (e.g., A): ").strip()
    valid = False
    
    while not valid:
        try:
            valid = validate_record_type(record_type)
        except ValueError as e:
            print(f"Error: {e}")
            record_type = input("Enter the record type (e.g., A): ").strip()
        
    return valid

def get_encoding_type():
    """
    \nPrompts the user to enter an encoding type.
    
    :return: The encoding type entered by the user.
    """
    encoding_type = input("Enter the encoding type (e.g., Base16): ").strip()
    valid = False
    
    while not valid:
        try:
            valid = validate_encoding_type(encoding_type)
        except ValueError as e:
            print(f"Error: {e}")
            encoding_type = input("Enter the encoding type (e.g., Base16): ").strip()
    
    return valid

def print_dns_query(results):
    """
    \nPrints the DNS query.
    
    :param dns_query_active: The DNS query to print.
    """
    print("\nDNS Query:")
    print(f"Domain A: {results.A.value}")
    
def user_interface():
    """
    \nRuns the user interface for the DNS Query Tool.
    """
    print("\nWelcome to the DNS Query Tool!\n")
    
    try:
        dns_name = get_dns_name()
        record_type = get_record_type()
        encoding_type = get_encoding_type()
        
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")

    dns_query_active = get_dns_query(dns_name, record_type, encoding_type)
    results = dns_resolution(dns_query_active)
    print_dns_query(results)


if __name__ == "__main__":
    user_interface() # run the user interface

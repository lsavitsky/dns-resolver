import sys 

sys.path.append("dns_servers/DNS_Query/dns_construction/")
import DNS_Tunnel_enums



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

        # Prompt for the DNS name
        dns_name = input("Enter the DNS name to query (e.g., example.com): ").strip()
        
        try:
            validate_dns_name(dns_name)
        except ValueError as e:
            print(f"Error: {e}")
        
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")

if __name__ == "__main__":
    main()

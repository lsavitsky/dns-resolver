import sys 

sys.path.append("./dns_servers/DNS_Query/dns_construction/")
print(sys.path)
import DNS_Tunnel_enums



def validate_dns_name(dns_name):
    """
    Validates the DNS name format.
    
    :param dns_name: The DNS name to validate.
    :return: True if the DNS name is valid, False otherwise.
    """
    labels = dns_name.split(".")
    
    if len(labels) < 2:
        raise ValueError("DNS name must have at least two labels.")
    
    tld = labels[-1]
    if not DNS_Tunnel_enums.EncodingType.is_valid_name(tld):
        raise ValueError(f"Invalid TLD: {tld}")
    
    return True

def main():
    try:
        print("\nWelcome to the DNS Query Tool!\n")

        # Prompt for the DNS name
        dns_name = input("Enter the DNS name to query (e.g., example.com): ").strip()
        try:
            if validate_dns_name(dns_name):
                print(f"Valid DNS name: {dns_name}")
                
        except dns.name.LabelError:
            print("Invalid DNS name format. Please try again.")
            return
        
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        
if __name__ == "__main__":
    main()
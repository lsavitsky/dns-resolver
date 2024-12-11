import time
import csv
import argparse
import os 

from controller import *

# result_dir 
result_dir = "results"
os.makedirs(result_dir, exist_ok=True)


def test_encoding(dns_name, record_type, encoding_type, output_file="dns_timing_results.csv"):
    """
    \nTests the encoding of a DNS query.
    
    :param dns_name: The DNS name to query.
    :param record_type: The record type to query.
    :param encoding_type: The encoding type to query.
    :param output_file: The output file to save the results (default: dns_timing_results.csv).
    
    :return: None 
    """
    encodePacketStart=time.perf_counter() # For data Collection 
    dns_query_active = get_dns_query(dns_name, record_type, encoding_type)
    encodePacketEnd =time.perf_counter() # For data Collection
    
    dnsResStart=time.perf_counter()
    dns_resolution(dns_query_active)
    dnsResEnd=time.perf_counter()
    
    output_file = os.path.join(result_dir, output_file)

    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        encode_duration = encodePacketEnd - encodePacketStart
        dns_resolution_duration = dnsResEnd - dnsResStart
        total_duration = dnsResEnd - encodePacketStart
        
    
        if file.tell() == 0: #IF needed write header
            writer.writerow([
                "domain", "record_type", "encoding_type",
                "encodePacketStart", "encodePacketEnd", "dnsResStart", "dnsResEnd", "encode_duration","dns_resolution_duration", "total_duration" ])
        
        writer.writerow([dns_name, record_type, encoding_type,
            encodePacketStart, encodePacketEnd, dnsResStart, dnsResEnd, encode_duration, dns_resolution_duration, total_duration])
        
def test_simulated_encoding(dns_name, record_type, encoding_type, num_iterations=1, output_file="dns_timing_results.csv"):
    """Test the encoding of a DNS query.
    
    :param dns_name: The DNS name to query.
    :param record_type: The record type to query.
    :param encoding_type: The encoding type to query.
    :param num_iterations: The number of iterations to run the test (default: 1).
    :param output_file: The output file to save the results (default: dns_timing_results.csv).
    
    :return: None
    """
    print(f"Testing encoding for {num_iterations} iterations...")
    print(f"DNS name: {dns_name}")
    print(f"Record type: {record_type}")
    print(f"Encoding type: {encoding_type}")
    
    for _ in range(num_iterations):
        test_encoding(dns_name, record_type, encoding_type, output_file)
    
def get_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(description='Run data preprocessing with specified parameters.')
    parser.add_argument('dns_name', type=validate_dns_name, help='The DNS name to query (e.g., example.com).')
    parser.add_argument('record_type', type=validate_record_type, help='The record type to query (e.g., A).')
    parser.add_argument('encoding_type', type=validate_encoding_type, help='The encoding type to query (e.g., Base16).')
    parser.add_argument('--num_iterations', type=int, default=1, help='The number of iterations to run the test.')
    parser.add_argument('--output_file', type=str, default="dns_timing_results.csv", help='The output file to save the results.')
    args = parser.parse_args()
    
    return args

def main():
    args = get_arguments()
    test_simulated_encoding(args.dns_name, args.record_type, args.encoding_type, args.num_iterations)
    
if __name__ == "__main__":
    main()
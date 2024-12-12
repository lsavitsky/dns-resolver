from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse
import csv
import sys
import os

"""
    User controller for advanced webserver hosting 
    Work in progress for more interesting user handling. Currently,
    Not functional
"""

class HtmlFileServer:
    def __init__(self, html_file, ip, port=8000):
        self.html_file = html_file
        self.ip = ip
        self.port = port
    def __str__(self):
        return f"HtmlFileServer(html_file={self.html_file}, ip={self.ip}, port={self.port})"

    def start_server(self):
        print(self)
        os.chdir(os.path.dirname(self.html_file))
        handler = SimpleHTTPRequestHandler
        server_address = (self.ip, self.port)
        httpd = HTTPServer((server_address), handler)
        print(f"Serving {self.html_file} at http://{self.ip}:{self.port}")
        try:
            httpd.serve_forever()
        except Exception as e:
            print(f"Error: {e}. Could not start the webserver.")
            sys.exit(1)


class WebServerManager:
    def __init__(self, directory, mapping):
        self.directory = directory
        self.mapping = mapping

    def __str__(self):
        """
            nicely formated string
        """
        return f"WebServerManager(directory={self.directory}, mapping={self.mapping})"
    def simple_hosting(self, html_file, ip):
        """
        simple_hosting - Call the method to host a single HTML file
        """
        print(self)
        server = HtmlFileServer(os.path.join(self.directory, html_file), ip)
        server.start_server()

    def dynamic_hosting(self):
        """
        dynamic_hosting - Call the method to host multiple HTML files 
        """
        for html_file in os.listdir(self.directory):
            if html_file.endswith(".html"):  # Must end with the right extension
                ip = self.mapping[html_file]
                self.simple_hosting(html_file, ip)  # Call simple hosting in loop

def dynamic_or_single(choice: str):
    """
    dynamic_or_single asks user if they are SURE they want to host ALL html files or not. Also turns into true/false.
    """
    if choice.strip().lower() == "dynamic":
        print("WARNING: Dynamic can require severe overhead on your device. If selection is NO, it will only host the ONE html file.")
        choice = input("Are you SURE? ").strip().lower()
        
    return choice == "dynamic"

def parse_html_mapper(html_mapper): 
    """
    Allow for multiple input types for the parser.
    """
    try:
        if ":" in html_mapper:
            return dict(item.split(":") for item in html_mapper.split(","))  # Splits on input if command line gave non-file
        else:
            mapping = {}
            try:
                # Open CSV file
                with open(html_mapper, mode='r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        ip, domain = row
                        mapping[domain] = ip
            except FileNotFoundError:
                new_file = input("File not found. Please enter the correct path to the CSV file: ").strip()
                try:
                    # Try again with new file path
                    with open(new_file, mode='r') as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            ip, domain = row
                            mapping[domain] = ip
                except Exception as e:
                    # Error processing file
                    print(f"Error: {e}. Couldn't process the file. Please check and rerun the script.")
                    sys.exit(1)
            return mapping
    except Exception as e:
        # General error
        print(f"Error: {e}. Please check your input and rerun the script.")
        sys.exit(1)

def main(): 
    parser = argparse.ArgumentParser(description="User controller for advanced webserver hosting.")
    parser.add_argument("html_directory_location", type=str, help="The path to the HTML files directory")
    parser.add_argument("mode", type=str, choices=["dynamic", "single"], help="Mode of hosting: 'dynamic' for all HTML files or 'single' for one HTML file")
    parser.add_argument("html_mapper", type=str, help="Path to a CSV file with IP to domain mappings, or IP:domain mappings directly")

    # Parse arguments to variables for ease of use
    args = parser.parse_args()
    directory = args.html_directory_location
    choice = args.mode
    html_mapper = args.html_mapper
    mapping = parse_html_mapper(html_mapper)
    server_manager = WebServerManager(directory, mapping)  # Create object for the server management 
    if dynamic_or_single(choice):  # Yes they are crazy enough to host all the webservers at once
        server_manager.dynamic_hosting()
    else:  # A single html
        for ip, html_file in mapping.items():
            server_manager.simple_hosting(html_file, ip)

if __name__ == "__main__":
    main()

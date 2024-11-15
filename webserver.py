"""
References: https://hackernoon.com/how-to-set-up-a-local-dns-server-with-python
"""
#http_server.py

import http.server
import socketserver

PORT = 8080 # Designation 
DIRECTORY = "html_files"
# Creates a HTTP Server hosting pur html file
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler): 
    def do_GET(self):
        if self.path == '/a.com':
            self.path = '/a.html'
        elif self.path == '/b.com':
            self.path = '/b.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def translate_path(self, path):
        return f"./{DIRECTORY}/{path}"

handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("0.0.0.0", PORT), handler_object)

print(f"Serving HTTP on port {PORT}")
my_server.serve_forever()
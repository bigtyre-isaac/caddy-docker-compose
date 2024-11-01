import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Retrieve environment variables for response code and message
response_code = int(os.getenv("RESPONSE_CODE", 200))
response_message = os.getenv("RESPONSE_MESSAGE", "Hello, World!").encode()

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(response_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message)

    def do_POST(self):
        self.do_GET()  # Respond the same way to all HTTP methods

    def do_PUT(self):
        self.do_GET()

    def do_DELETE(self):
        self.do_GET()

if __name__ == "__main__":
    # Set up the HTTP server
    server_address = ("", 80)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"Serving on port 80 with response code {response_code} and message '{response_message.decode()}'")
    httpd.serve_forever()

import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

# Set up logging to output to console
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

logger.info("Server starting...")

# Retrieve environment variables for response code and message
response_code = int(os.getenv("RESPONSE_CODE", 200))
response_message = os.getenv("RESPONSE_MESSAGE", "Hello, World!").encode()

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info("Received GET request")
        self.send_response(response_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message)

    def do_POST(self):
        logger.info("Received POST request")
        self.do_GET()

    def do_PUT(self):
        logger.info("Received PUT request")
        self.do_GET()

    def do_DELETE(self):
        logger.info("Received DELETE request")
        self.do_GET()

logger.info(f"Thread started: {__name__}")

if __name__ == "__main__":
    logger.info("Started listening for requests on port 80")
    # Set up the HTTP server
    server_address = ("", 80)
    httpd = HTTPServer(server_address, CustomHandler)
    logger.info(f"Serving on port 80 with response code {response_code} and message '{response_message.decode()}'")
    httpd.serve_forever()

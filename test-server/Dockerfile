# Start with a lightweight Python image
FROM python:3.10-slim

# Set default environment variables (can be overridden)
ENV RESPONSE_CODE=200
ENV RESPONSE_MESSAGE="Hello, World!"

# Copy the server script into the image
COPY server.py /server.py

# Run the web server on port 80
CMD ["python3", "/server.py"]

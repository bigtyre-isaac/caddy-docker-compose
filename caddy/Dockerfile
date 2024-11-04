# Use the official Caddy image as the base
FROM caddy:2

# Copy all static files and handle_errors configuration
#COPY static /usr/share/caddy/static
COPY static /srv/static
COPY handle_errors.caddy /etc/caddy/handle_errors.caddy
COPY generate_caddyfile.sh /tmp/generate_caddyfile.sh

# Make the script executable
RUN chmod +x /tmp/generate_caddyfile.sh && ls -l /tmp/generate_caddyfile.sh

# Run the script to generate the Caddyfile and start Caddy
ENTRYPOINT ["/bin/sh", "-c", "/tmp/generate_caddyfile.sh && caddy run --config /etc/caddy/Caddyfile"]

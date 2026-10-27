# Use the official Caddy image as the base
FROM caddy:2.11.7-alpine

LABEL org.opencontainers.image.title="Caddy Application Proxy" \
      org.opencontainers.image.description="Serve multiple applications under one domain using environment-based routes instead of manually editing a Caddyfile." \
      org.opencontainers.image.url="https://github.com/bigtyre-isaac/caddy-docker-compose" \
      org.opencontainers.image.source="https://github.com/bigtyre-isaac/caddy-docker-compose" \
      org.opencontainers.image.documentation="https://github.com/bigtyre-isaac/caddy-docker-compose#readme"

# Copy all static files and handle_errors configuration
#COPY static /usr/share/caddy/static
COPY static /srv/static
COPY handle_errors.caddy /etc/caddy/handle_errors.caddy
COPY generate_caddyfile.sh /tmp/generate_caddyfile.sh

# Make the script executable
RUN chmod +x /tmp/generate_caddyfile.sh && ls -l /tmp/generate_caddyfile.sh

# Run the script to generate the Caddyfile and start Caddy
ENTRYPOINT ["/bin/sh", "-c", "/tmp/generate_caddyfile.sh && caddy run --config /etc/caddy/Caddyfile"]

# Use the official Caddy image as the base
FROM caddy:2

COPY generate_caddyfile.sh /tmp/generate_caddyfile.sh

RUN chmod +x /tmp/generate_caddyfile.sh && ls -l /tmp/generate_caddyfile.sh

ENTRYPOINT ["/bin/sh", "-c", "/tmp/generate_caddyfile.sh && caddy run --config /etc/caddy/Caddyfile"]

#!/bin/sh

# Output Caddyfile location
CADDYFILE_PATH="/etc/caddy/Caddyfile"

HOST="${HOST:-:80}"

# Start with the server block definition
echo "$HOST {" > $CADDYFILE_PATH

# Global headers to apply to all requests
cat <<EOF >> $CADDYFILE_PATH
  header {
    Host {http.request.host}
    X-Real-IP {http.request.remote}
  }

  import /etc/caddy/handle_errors.caddy
  
EOF

# Iterate over environment variables that start with "ROUTE_" or "PATH_"
for var in $(env | grep -E '^ROUTE_|^PATH_'); do
  # Extract the key and value
  key=$(echo "$var" | cut -d'=' -f1)
  value=$(echo "$var" | cut -d'=' -f2-)

  # Get the path by stripping the prefix (ROUTE_ or PATH_)
  path=$(echo "$key" | sed 's/^ROUTE_//;s/^PATH_//')
  path="/${path}/*" # Append /* to match all subpaths

  # Determine the directive (route or handle_path) based on the prefix
  if [[ $key == ROUTE_* ]]; then
    directive="route"
  elif [[ $key == PATH_* ]]; then
    directive="handle_path"
  fi

  # Add the route or handle_path block to the Caddyfile
  cat <<EOF >> $CADDYFILE_PATH
  $directive $path {
    reverse_proxy $value
  }
  
EOF
done

# Check if ROOT variable exists and set up a default reverse proxy for it
if [ -n "$ROOT" ]; then
  cat <<EOF >> $CADDYFILE_PATH
  reverse_proxy $ROOT
EOF
fi



# Close the server block
echo "}" >> $CADDYFILE_PATH

echo 'Caddyfile generated'
echo '---------------------'
cat $CADDYFILE_PATH
echo '---------------------'
echo ''

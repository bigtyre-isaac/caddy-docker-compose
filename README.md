# Caddy Docker Compose

A Caddy application proxy for serving multiple applications under one domain, such as `example.com/app1/` and `example.com/app2/`, **using environment variables to configure routes instead of manually editing a Caddyfile**.

Define each application's path and upstream service in your container configuration. The proxy generates the Caddyfile on startup, with support for stripping or preserving path prefixes, a default upstream, and a custom error page when an upstream is unavailable.

## Configuration

Set these environment variables on the proxy service:

| Variable | Purpose | Example |
| --- | --- | --- |
| `HOST` | Caddy site address; defaults to `:80`. | `:80` |
| `ROOT` | Default upstream(s) for requests that do not match a route. Separate multiple upstreams with spaces. | `app:8080 app2:8080` |
| `PATH_<path>` | Forward `/<path>/*`, removing the prefix before sending the request upstream. | `PATH_api=api:8080` |
| `ROUTE_<path>` | Forward `/<path>/*`, keeping the original request path. | `ROUTE_files=files:8080` |

For example:

```yaml
environment:
  HOST: ":80"
  ROOT: "app:8080"
  PATH_app1: "app1:8080"
  PATH_app2: "app2:8080"
```

This serves `example.com/app1/` from `app1:8080` and `example.com/app2/` from `app2:8080`, stripping each application's prefix before forwarding. For example, `/app1/users` becomes `/users` on `app1:8080`. Other requests go to `app:8080`. Use `ROUTE_` instead of `PATH_` when an application expects to receive its prefix.

Upstream names must be reachable from the proxy container. Services on the same Docker network can use their Compose service names. Ports default to 80 when omitted.

Routes match a trailing slash and anything after it: `/api/` matches, but `/api` falls through to `ROOT`. When using multiple default upstreams, use the YAML mapping syntax above so quotes do not become part of the environment value.

Customize error handling in `caddy/handle_errors.caddy` and the 502 page in `caddy/static/errors/502-error.html`.

## Usage

Build the image from the `caddy` directory:

```sh
docker build -t caddy-proxy ./caddy
```

Run it on the same network as your upstream services, publishing port 80 and supplying your routes. For example, with an existing `app-network` and an upstream named `app`:

```sh
docker run -d --name proxy --network app-network -p 8088:80 -e ROOT=app:8080 caddy-proxy
```

Requests to `http://localhost:8088/` now go to `app:8080`. Recreate the container after changing environment variables; rebuild the image after changing the generator or error pages.

Keep shell scripts saved with LF line endings. `.gitattributes` enforces LF on Git checkouts to prevent `/bin/sh: ...: not found` errors.

## Testing

The top-level `docker-compose.yml` runs the proxy and two small Python backends. Start the example with:

```sh
docker compose up --build -d
```

- `http://localhost:8088/` — load balances between both backends.
- `http://localhost:8088/server1/` — backend 1.
- `http://localhost:8088/server2/` — backend 2.

Set `RESPONSE_CODE` and `RESPONSE_MESSAGE` on either backend to try different responses. Use `docker compose down` to stop the example.

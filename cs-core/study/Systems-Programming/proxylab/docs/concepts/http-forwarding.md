# HTTP Forwarding

The proxy in this project only supports the most important baseline case:

- absolute-form `GET` requests
- rewritten as `HTTP/1.0` on the outbound side

## URI Parsing

The request line contains a full URI, for example:

```text
GET http://127.0.0.1:18080/cacheable/basic HTTP/1.1
```

The proxy extracts:

- host
- port, defaulting to `80`
- path, defaulting to `/`

That split is enough to open a server connection and rebuild the outbound request.

## Header Policy

The outbound request always includes:

- `Host`
- the fixed CS:APP `User-Agent`
- `Connection: close`
- `Proxy-Connection: close`

Client-supplied values for those headers are ignored.
Other headers are forwarded unchanged.

This is important because the proxy is not trying to preserve arbitrary client connection semantics.
It is trying to behave like the lab expects: one request per upstream connection, explicit close.

## Error Policy

The study implementation returns simple text errors for:

- malformed request lines
- unsupported methods
- upstream connection failures

That is enough to verify robustness without turning the project into a full HTTP server exercise.

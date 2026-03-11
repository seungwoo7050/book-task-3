# URL Parsing for HTTP Proxies

## HTTP URL Structure

An HTTP URL follows this structure:

```
http://hostname:port/path
```

| Component | Required | Default | Example |
| :--- | :--- | :--- | :--- |
| Scheme | Yes | — | `http://` |
| Hostname | Yes | — | `www.example.com` |
| Port | No | `80` | `:8080` |
| Path | No | `/` | `/index.html` |

## Parsing Algorithm

Given a URL like `http://www.example.com:8080/path/to/resource`:

```python
def parse_url(url: str) -> tuple[str, int, str]:
    """Parse an absolute HTTP URL.

    Args:
        url: Full URL (e.g., "http://www.example.com:8080/index.html")

    Returns:
        (hostname, port, path)
    """
    # Step 1: Remove the scheme
    # "http://www.example.com:8080/index.html" → "www.example.com:8080/index.html"
    url = url.replace("http://", "", 1)

    # Step 2: Split host and path
    if "/" in url:
        host_port, path = url.split("/", 1)
        path = "/" + path
    else:
        host_port = url
        path = "/"

    # Step 3: Split host and port
    if ":" in host_port:
        hostname, port_str = host_port.split(":", 1)
        port = int(port_str)
    else:
        hostname = host_port
        port = 80

    return hostname, port, path
```

## Examples

| Input URL | Hostname | Port | Path |
| :--- | :--- | :--- | :--- |
| `http://www.example.com/index.html` | `www.example.com` | `80` | `/index.html` |
| `http://www.example.com:8080/page` | `www.example.com` | `8080` | `/page` |
| `http://www.example.com/` | `www.example.com` | `80` | `/` |
| `http://www.example.com` | `www.example.com` | `80` | `/` |
| `http://host.com/a/b/c?q=1` | `host.com` | `80` | `/a/b/c?q=1` |

## Extracting the URL from a Proxy Request

A proxy receives requests with absolute URLs:

```
GET http://www.example.com/index.html HTTP/1.1\r\n
Host: www.example.com\r\n
...
```

To extract the URL:

```python
request_line = "GET http://www.example.com/index.html HTTP/1.1"
parts = request_line.split()
method = parts[0]    # "GET"
url = parts[1]       # "http://www.example.com/index.html"
version = parts[2]   # "HTTP/1.1"
```

## Building the Forwarded Request

After parsing, construct a request with a **relative path** for the origin server:

```python
hostname, port, path = parse_url(url)

forwarded_request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {hostname}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)
```

The key difference: the proxy request uses `http://hostname/path` while the forwarded request uses just `/path`.

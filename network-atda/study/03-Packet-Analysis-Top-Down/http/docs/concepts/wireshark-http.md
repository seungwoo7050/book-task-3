# Wireshark HTTP Analysis Techniques

## Display Filters for HTTP

Wireshark display filters allow you to isolate specific traffic from a capture. HTTP filters operate on the `http` protocol dissector.

### Basic Filters

| Filter | Description |
| :--- | :--- |
| `http` | All HTTP traffic (requests and responses) |
| `http.request` | Only HTTP requests |
| `http.response` | Only HTTP responses |
| `http.request.method == "GET"` | Only GET requests |
| `http.response.code == 200` | Only 200 OK responses |
| `http.response.code == 304` | Only 304 Not Modified responses |
| `http.host == "gaia.cs.umass.edu"` | Requests to a specific host |

### Combining Filters

| Operator | Symbol | Example |
| :--- | :--- | :--- |
| AND | `&&` | `http.request && ip.dst == 128.119.245.12` |
| OR | `\|\|` | `http.response.code == 200 \|\| http.response.code == 304` |
| NOT | `!` | `!http.request.method == "OPTIONS"` |

### Content Filters

| Filter | Description |
| :--- | :--- |
| `http.content_type contains "text/html"` | Responses with HTML content |
| `http.request.uri contains ".jpg"` | Requests for JPEG images |
| `http.referer contains "example.com"` | Requests referred from example.com |
| `http.content_length > 1000` | Responses larger than 1KB |

## Step-by-Step Analysis Workflow

### 1. Open the Trace File

```bash
wireshark http-basic.pcapng
```

### 2. Apply a Display Filter

Type `http` in the display filter toolbar and press **Enter**. This hides non-HTTP packets.

### 3. Identify the HTTP Request

- Look for a row where the **Info** column shows `GET /path HTTP/1.1`
- Click on the row to select it
- In the **Packet Details** pane, expand **Hypertext Transfer Protocol**
- You'll see the request line, headers, and (if POST) body

### 4. Identify the HTTP Response

- The response typically follows the request by a few packets
- The **Info** column shows `HTTP/1.1 200 OK` (or another status code)
- Expand **Hypertext Transfer Protocol** to see response headers
- The **Packet Bytes** pane shows the raw ASCII of the response

### 5. Follow the TCP Stream

For a complete picture of the HTTP exchange:
1. Right-click on any HTTP packet
2. Select **Follow → TCP Stream**
3. This shows the full request-response exchange as colored text:
   - **Red** = data sent by the client (request)
   - **Blue** = data sent by the server (response)

### 6. Extract Field Values

To quickly extract specific fields for multiple packets:

```bash
tshark -r http-basic.pcapng -Y "http" -T fields \
    -e frame.number \
    -e http.request.method \
    -e http.request.uri \
    -e http.response.code \
    -e http.content_length
```

## Reassembled HTTP

When HTTP responses are larger than a single TCP segment:
- Wireshark shows `[TCP segment of a reassembled PDU]` for intermediate segments
- The final segment shows the complete reassembled HTTP response
- Check the **Reassembled TCP** section at the bottom of the packet details

To see the reassembly details:
1. Click on the HTTP response packet (not a TCP segment)
2. Look for **[x reassembled TCP segments]** in the details pane
3. This tells you how many TCP segments were combined

## Key Shortcuts

| Action | Shortcut |
| :--- | :--- |
| Apply display filter | `Enter` (in filter bar) |
| Clear display filter | `Ctrl+Backspace` |
| Follow TCP stream | Right-click → Follow → TCP Stream |
| Go to packet number | `Ctrl+G` |
| Find packet | `Ctrl+F` |
| Time reference | `Ctrl+T` (set selected packet as time zero) |
| Column preferences | Right-click column header → Column Preferences |

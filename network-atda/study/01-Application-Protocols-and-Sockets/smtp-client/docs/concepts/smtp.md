# SMTP Protocol Reference

## Overview

**SMTP** (Simple Mail Transfer Protocol) is the standard application-layer protocol for sending email across the Internet. Defined in **RFC 5321**, SMTP operates over **TCP** (typically port 25, 587, or 465) and uses a **command-response** model.

The client (Mail User Agent or MUA) connects to the server (Mail Transfer Agent or MTA), issues a series of text commands, and the server replies with numeric status codes.

## SMTP Dialogue Flow

```
Client                                 Server
  |                                      |
  |  ---- TCP connect ----------------> |
  |  <--- 220 Welcome ----------------  |  (1) Greeting
  |                                      |
  |  ---- HELO hostname --------------> |  (2) Handshake
  |  <--- 250 OK ---------------------  |
  |                                      |
  |  ---- MAIL FROM:<sender> ---------> |  (3) Envelope sender
  |  <--- 250 OK ---------------------  |
  |                                      |
  |  ---- RCPT TO:<recipient> --------> |  (4) Envelope recipient
  |  <--- 250 OK ---------------------  |
  |                                      |
  |  ---- DATA -----------------------> |  (5) Begin message
  |  <--- 354 Start mail input -------  |
  |                                      |
  |  ---- From: sender              --> |  (6) Message headers + body
  |  ---- To: recipient             --> |
  |  ---- Subject: Test             --> |
  |  ----                           --> |
  |  ---- This is the body.         --> |
  |  ---- .                         --> |  (7) End-of-data marker
  |  <--- 250 OK ---------------------  |
  |                                      |
  |  ---- QUIT -----------------------> |  (8) Close session
  |  <--- 221 Bye --------------------  |
```

## SMTP Commands

| Command | Syntax | Purpose |
| :--- | :--- | :--- |
| `HELO` | `HELO <domain>` | Identify the client to the server |
| `EHLO` | `EHLO <domain>` | Extended HELO (supports SMTP extensions) |
| `MAIL FROM` | `MAIL FROM:<address>` | Specify the sender's email address |
| `RCPT TO` | `RCPT TO:<address>` | Specify the recipient's email address |
| `DATA` | `DATA` | Begin the message body transfer |
| `QUIT` | `QUIT` | End the SMTP session |
| `RSET` | `RSET` | Reset the current transaction |
| `NOOP` | `NOOP` | No operation (keep-alive) |
| `AUTH` | `AUTH LOGIN` | Begin authentication (extension) |
| `STARTTLS` | `STARTTLS` | Upgrade to encrypted connection |

### Important: All commands must be terminated with `\r\n`

## SMTP Reply Codes

Reply codes are 3-digit numbers. The first digit indicates the category:

| First Digit | Category | Meaning |
| :--- | :--- | :--- |
| `2xx` | Positive completion | Command accepted and completed |
| `3xx` | Positive intermediate | Command accepted, waiting for more input |
| `4xx` | Transient failure | Temporary error, try again later |
| `5xx` | Permanent failure | Command rejected, do not retry |

### Common Reply Codes

| Code | Meaning |
| :--- | :--- |
| `220` | Service ready (server greeting) |
| `221` | Service closing transmission channel |
| `235` | Authentication successful |
| `250` | Requested action completed |
| `334` | Server challenge (for AUTH) |
| `354` | Start mail input; end with `<CRLF>.<CRLF>` |
| `421` | Service not available |
| `450` | Mailbox unavailable (temporary) |
| `500` | Syntax error, command unrecognized |
| `501` | Syntax error in parameters |
| `503` | Bad sequence of commands |
| `550` | Mailbox unavailable (permanent) |

## Sending Commands in Python

```python
import socket

def send_command(sock, command):
    """Send an SMTP command and return the reply."""
    print(f"C: {command}")
    sock.sendall(f"{command}\r\n".encode())
    reply = sock.recv(4096).decode()
    print(f"S: {reply.strip()}")
    return reply
```

## End-of-Data Marker

The DATA command body is terminated by a line containing **only a single period** (`.`):

```
\r\n.\r\n
```

If the message body contains a line starting with `.`, it must be "dot-stuffed" by prepending an additional `.` (e.g., `..`). For this assignment, simple messages without leading dots are sufficient.

## STARTTLS (Optional)

To encrypt the SMTP connection:

```python
import ssl

# After EHLO, send STARTTLS
send_command(sock, "STARTTLS")
# Wrap the socket in TLS
context = ssl.create_default_context()
sock = context.wrap_socket(sock, server_hostname=server)
# Re-issue EHLO after TLS upgrade
send_command(sock, f"EHLO {hostname}")
```

## AUTH LOGIN (Optional)

For servers requiring authentication:

```python
import base64

send_command(sock, "AUTH LOGIN")
# Server sends 334 (base64-encoded "Username:")
send_command(sock, base64.b64encode(username.encode()).decode())
# Server sends 334 (base64-encoded "Password:")
send_command(sock, base64.b64encode(password.encode()).decode())
# Server sends 235 (authentication successful)
```

## Testing Locally

Python provides a built-in debugging SMTP server that prints received messages to the console without actually delivering them:

```bash
# Start a local debug server on port 1025
python3 -m smtpd -n -c DebuggingServer localhost:1025
```

This is the recommended way to test your client without configuring a real mail server.

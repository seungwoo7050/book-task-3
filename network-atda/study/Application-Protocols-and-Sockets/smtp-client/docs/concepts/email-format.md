# Email Message Format

## Overview

An email message (as defined by **RFC 5322**) consists of two parts separated by a blank line:

1. **Headers**: Metadata about the message (From, To, Subject, Date, etc.)
2. **Body**: The actual message content

```
From: alice@example.com\r\n
To: bob@example.com\r\n
Subject: Hello from SMTP Client\r\n
Date: Mon, 01 Jan 2024 12:00:00 +0000\r\n
\r\n                                     ← Blank line separates headers from body
This is the body of the email.\r\n
It can span multiple lines.\r\n
```

## Required Headers

| Header | Purpose | Example |
| :--- | :--- | :--- |
| `From` | Sender's display address | `From: Alice <alice@example.com>` |
| `To` | Recipient's display address | `To: Bob <bob@example.com>` |
| `Subject` | Message subject line | `Subject: Test Email` |

## Optional Headers

| Header | Purpose | Example |
| :--- | :--- | :--- |
| `Date` | Timestamp | `Date: Mon, 01 Jan 2024 12:00:00 +0000` |
| `Message-ID` | Unique message identifier | `Message-ID: <abc123@example.com>` |
| `MIME-Version` | MIME version | `MIME-Version: 1.0` |
| `Content-Type` | Body content type | `Content-Type: text/plain; charset=utf-8` |

## Envelope vs. Headers

There is an important distinction between **envelope addresses** (used by SMTP for routing) and **header addresses** (displayed to the user):

```
SMTP Envelope (routing):          Message Headers (display):
  MAIL FROM:<alice@example.com>     From: Alice <alice@example.com>
  RCPT TO:<bob@example.com>         To: Bob <bob@example.com>
```

These can be different! For this assignment, keep them the same for simplicity.

## Constructing a Message in Python

```python
sender = "alice@example.com"
recipient = "bob@example.com"
subject = "Test Email from SMTP Client"
body = "Hello! This email was sent using raw SMTP sockets."

message = (
    f"From: {sender}\r\n"
    f"To: {recipient}\r\n"
    f"Subject: {subject}\r\n"
    f"\r\n"
    f"{body}\r\n"
    f".\r\n"
)
```

The final `.\r\n` is the SMTP end-of-data marker — it tells the server that the message body is complete.

## Line Length

RFC 5322 recommends that lines in an email should not exceed **998 characters** (with CRLF). For practical purposes, keep lines under **78 characters** for readability.

## Character Encoding

- Headers must be ASCII (7-bit)
- For non-ASCII characters in headers, use RFC 2047 encoded words:
  `=?utf-8?B?base64_encoded?=`
- Body encoding depends on `Content-Type` and `Content-Transfer-Encoding` headers
- For this assignment, plain ASCII text is sufficient

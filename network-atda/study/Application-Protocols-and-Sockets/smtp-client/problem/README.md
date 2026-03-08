# SMTP Mail Client — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement an SMTP client that sends an email by directly speaking the SMTP protocol over a TCP socket. The client must handle the full SMTP command dialogue without relying on Python's built-in `smtplib`.

## Requirements

### Functional Requirements

1. **TCP Connection**
   - Connect to an SMTP server on the appropriate port
   - Read the server's initial `220` greeting

2. **SMTP Dialogue**
   The client must issue the following commands in order and verify each server reply:

   | Step | Client Sends | Expected Reply Code |
   | :--- | :--- | :--- |
   | 1 | `HELO <client_hostname>\r\n` | `250` |
   | 2 | `MAIL FROM:<sender@example.com>\r\n` | `250` |
   | 3 | `RCPT TO:<recipient@example.com>\r\n` | `250` |
   | 4 | `DATA\r\n` | `354` |
   | 5 | Message body ending with `\r\n.\r\n` | `250` |
   | 6 | `QUIT\r\n` | `221` |

3. **Email Message Format**
   - The DATA section must include at minimum:
     ```
     From: sender@example.com\r\n
     To: recipient@example.com\r\n
     Subject: Test Email\r\n
     \r\n
     This is the body of the email.\r\n
     .\r\n
     ```

4. **Error Handling**
   - After each command, check the reply code
   - If an unexpected code is received, print the error and terminate gracefully

5. **Optional: TLS Support**
   - Implement `STARTTLS` for encrypted communication
   - Implement `AUTH LOGIN` for server authentication

### Expected Output

```
Connecting to smtp.example.com:587 ...
S: 220 smtp.example.com ESMTP ready
C: HELO localhost
S: 250 Hello localhost
C: MAIL FROM:<alice@example.com>
S: 250 OK
C: RCPT TO:<bob@example.com>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: (sending message body)
S: 250 OK: queued
C: QUIT
S: 221 Bye
Email sent successfully!
```

## Constraints

- Python 3 standard library only
- `smtplib` is **not** allowed
- Primary modules: `socket`, `ssl` (for TLS), `base64` (for AUTH)

## Input / Environment

- Skeleton code: `code/smtp_client_skeleton.py`
- For local testing, use Python's built-in debugging SMTP server:
  ```bash
  python3 -m smtpd -n -c DebuggingServer localhost:1025
  ```
  Or the newer `aiosmtpd`:
  ```bash
  pip install aiosmtpd
  python3 -m aiosmtpd -n -l localhost:1025
  ```
- Test script: `script/test_smtp.sh`

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Complete SMTP Dialogue** | All required SMTP commands are sent in correct order |
| **Reply Code Validation** | Each server reply is checked before proceeding |
| **Message Delivery** | Email is successfully delivered (or logged by debug server) |
| **Error Handling** | Unexpected reply codes are caught and reported |
| **Code Quality** | Clean, well-documented code |

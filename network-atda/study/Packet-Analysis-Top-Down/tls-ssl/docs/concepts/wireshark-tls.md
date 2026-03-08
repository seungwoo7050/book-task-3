# Wireshark TLS Analysis Techniques

## Essential Display Filters

### General TLS Filters

```
tls                                    # All TLS traffic
tls.record                             # All TLS records
tls.handshake                          # All handshake messages
tls.alert                              # Alert messages
```

### By Handshake Message Type

```
tls.handshake.type == 1                # ClientHello
tls.handshake.type == 2                # ServerHello
tls.handshake.type == 11               # Certificate
tls.handshake.type == 12               # ServerKeyExchange
tls.handshake.type == 14               # ServerHelloDone
tls.handshake.type == 16               # ClientKeyExchange
tls.handshake.type == 20               # Finished
```

### By Record Content Type

```
tls.record.content_type == 20          # ChangeCipherSpec
tls.record.content_type == 21          # Alert
tls.record.content_type == 22          # Handshake
tls.record.content_type == 23          # Application Data
```

### By Version

```
tls.record.version == 0x0303           # TLS 1.2 record layer
tls.handshake.version == 0x0303        # TLS 1.2 handshake
tls.handshake.extensions.supported_version == 0x0304  # TLS 1.3
```

### By Extension

```
tls.handshake.extensions_server_name              # SNI present
tls.handshake.extensions_server_name == "example.com"  # Specific SNI
tls.handshake.extension.type == 0x0033            # key_share extension
tls.handshake.extension.type == 0x002b            # supported_versions
```

### By Cipher Suite

```
tls.handshake.ciphersuite == 0x1301    # TLS_AES_128_GCM_SHA256
tls.handshake.ciphersuite == 0xc02f    # TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

### Certificate Filters

```
tls.handshake.certificate              # Certificate data present
x509ce.dNSName                         # Certificate SAN DNS names
x509sat.utf8String                     # Certificate subject fields
```

### Combination Examples

```
# Complete handshake for a specific server
tls.handshake && ip.addr == 93.184.216.34

# Find ClientHello with specific SNI
tls.handshake.type == 1 && tls.handshake.extensions_server_name == "example.com"

# All encrypted application data to/from a server
tls.record.content_type == 23 && ip.addr == 93.184.216.34

# TLS 1.3 sessions only
tls.handshake.extensions.supported_version == 0x0304
```

## TLS Decryption in Wireshark

### Method 1: Pre-Master Secret Log (Recommended)

This works for all cipher suites including ephemeral key exchange.

#### Step 1: Capture Session Keys

```bash
# Set environment variable before launching browser
export SSLKEYLOGFILE=/path/to/sslkeylog.txt

# Launch Chrome
open -a "Google Chrome"

# Or launch Firefox
open -a "Firefox"
```

#### Step 2: Configure Wireshark

1. **Edit → Preferences → Protocols → TLS**
2. Set **(Pre)-Master-Secret log filename** to `/path/to/sslkeylog.txt`
3. Click **OK**

Wireshark will automatically decrypt any session whose keys are in the log file.

#### Key Log File Format

```
CLIENT_RANDOM <32-byte client random hex> <48-byte master secret hex>
```

Or for TLS 1.3:
```
CLIENT_HANDSHAKE_TRAFFIC_SECRET <client_random> <secret>
SERVER_HANDSHAKE_TRAFFIC_SECRET <client_random> <secret>
CLIENT_TRAFFIC_SECRET_0 <client_random> <secret>
SERVER_TRAFFIC_SECRET_0 <client_random> <secret>
```

### Method 2: RSA Private Key (Limited)

Only works for RSA key exchange (NOT ECDHE/DHE). Rarely applicable for modern TLS.

1. **Edit → Preferences → Protocols → TLS → RSA keys list**
2. Add: IP, Port, Protocol, Key file path

### Verifying Decryption

After configuring decryption:
- Encrypted Application Data records will show decrypted content
- A new "Decrypted TLS" tab appears in the packet details pane
- HTTP requests/responses become visible inside TLS records
- The protocol column may show "HTTP" instead of "TLS" for decrypted sessions

## Examining TLS Records in Wireshark

### Packet Detail Pane

When selecting a TLS packet, the detail pane shows:

```
▶ Transport Layer Security
  ▶ TLS Record Layer: Handshake Protocol: Client Hello
    Content Type: Handshake (22)
    Version: TLS 1.0 (0x0301)
    Length: 512
    ▶ Handshake Protocol: Client Hello
      Handshake Type: Client Hello (1)
      Length: 508
      Version: TLS 1.2 (0x0303)
      Random: a1b2c3d4...
      Session ID Length: 32
      Session ID: 5e6f7a8b...
      Cipher Suites Length: 42
      Cipher Suites (21 suites)
        Cipher Suite: TLS_AES_128_GCM_SHA256 (0x1301)
        Cipher Suite: TLS_AES_256_GCM_SHA384 (0x1302)
        ...
      ▶ Extensions
        ▶ Extension: server_name (len=14)
          Server Name: example.com
        ▶ Extension: supported_versions (len=5)
          Supported Version: TLS 1.3 (0x0304)
          Supported Version: TLS 1.2 (0x0303)
```

### Multiple Records per TCP Segment

A single TCP segment may contain multiple TLS records. Wireshark shows all of them:

```
▶ Transport Layer Security
  ▶ TLS Record Layer: Handshake Protocol: Server Hello
  ▶ TLS Record Layer: Change Cipher Spec
  ▶ TLS Record Layer: Handshake Protocol: Encrypted Handshake Message
```

## tshark Commands for TLS Analysis

### List All TLS Handshakes

```bash
tshark -r capture.pcap -Y "tls.handshake" \
    -T fields -e frame.number -e ip.src -e ip.dst \
    -e tls.handshake.type -e tls.handshake.version
```

### Extract SNI from ClientHellos

```bash
tshark -r capture.pcap -Y "tls.handshake.type == 1" \
    -T fields -e ip.dst -e tls.handshake.extensions_server_name | sort -u
```

### List Negotiated Cipher Suites

```bash
tshark -r capture.pcap -Y "tls.handshake.type == 2" \
    -T fields -e frame.number -e tls.handshake.ciphersuite
```

### Extract Certificate Information

```bash
tshark -r capture.pcap -Y "tls.handshake.type == 11" \
    -T fields -e frame.number -e x509sat.utf8String -e x509ce.dNSName
```

### Count TLS Record Types

```bash
tshark -r capture.pcap -Y "tls" \
    -T fields -e tls.record.content_type | sort | uniq -c | sort -rn
```

## Troubleshooting

### "Application Data" shows encrypted bytes only
- Decryption is not configured or keys don't match
- Ensure SSLKEYLOGFILE was set BEFORE the TLS session was established
- Verify the key log file contains entries for the session's client_random

### "Handshake Failure" alert
- Client and server couldn't agree on cipher suite or TLS version
- Check ClientHello cipher suites vs server requirements

### TLS record version shows 1.0 but session is 1.2/1.3
- Normal behavior: The record layer version in ClientHello is often 0x0301 (TLS 1.0) for compatibility
- The actual negotiated version is in the ServerHello handshake version or supported_versions extension

### Cannot see Certificate details
- If the session is TLS 1.3, certificates are encrypted after ServerHello
- Decryption is required to see certificate contents in TLS 1.3

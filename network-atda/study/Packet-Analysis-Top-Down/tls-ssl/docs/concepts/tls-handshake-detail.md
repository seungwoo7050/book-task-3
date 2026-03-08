# TLS Handshake Detail

## ClientHello Message

The first message of the TLS handshake, sent by the client.

### Structure

| Field | Description |
|-------|-------------|
| Handshake Type | 1 (ClientHello) |
| Client Version | Maximum TLS version supported (or 0x0303 for TLS 1.3 with supported_versions extension) |
| Random | 32 bytes of client-generated random data (used in key derivation) |
| Session ID | For session resumption (may be empty or contain a previous session ID) |
| Cipher Suites | Ordered list of cipher suites the client supports (most preferred first) |
| Compression Methods | Supported compression (always includes null; TLS 1.3 only allows null) |
| Extensions | Variable-length list of TLS extensions |

### Important Extensions

| Extension | ID | Description |
|-----------|----|-------------|
| server_name (SNI) | 0 | The hostname the client is connecting to (allows virtual hosting) |
| supported_groups | 10 | Elliptic curves or DH groups the client supports |
| signature_algorithms | 13 | Signature algorithms the client accepts for certificates |
| supported_versions | 43 | Actual TLS versions supported (TLS 1.3+) |
| key_share | 51 | Client's public key shares for key agreement (TLS 1.3) |
| psk_key_exchange_modes | 45 | Pre-shared key modes (TLS 1.3 resumption) |
| application_layer_protocol_negotiation (ALPN) | 16 | Application protocols the client supports (e.g., h2, http/1.1) |
| ec_point_formats | 11 | Supported elliptic curve point formats |
| session_ticket | 35 | Session ticket for stateless resumption |
| status_request (OCSP) | 5 | Request for certificate status (OCSP stapling) |

### SNI (Server Name Indication)

SNI is critical for HTTPS on shared hosting. The client sends the target hostname in plaintext within the ClientHello, allowing the server to present the correct certificate. This is visible even without TLS decryption.

Note: Encrypted ClientHello (ECH) in TLS 1.3 extensions encrypts the SNI, but it is not yet widely deployed.

## ServerHello Message

The server's response selecting parameters for the session.

### Structure

| Field | Description |
|-------|-------------|
| Handshake Type | 2 (ServerHello) |
| Server Version | Negotiated TLS version |
| Random | 32 bytes of server-generated random data |
| Session ID | Session identifier (may echo client's or generate new) |
| Cipher Suite | The single cipher suite selected from the client's list |
| Compression Method | Selected compression (always null) |
| Extensions | Server extensions (e.g., supported_versions, key_share) |

## Certificate Message

Sent by the server (and optionally by the client) to provide the certificate chain.

### Certificate Chain Structure

```
┌─────────────────────────────┐
│ Leaf (Server) Certificate   │  ← Server's own certificate
├─────────────────────────────┤
│ Intermediate CA Certificate │  ← Signed by Root CA
├─────────────────────────────┤
│ (Optional) Root Certificate │  ← Self-signed, usually NOT sent
└─────────────────────────────┘
```

### X.509 Certificate Fields

| Field | Description |
|-------|-------------|
| Version | Certificate version (usually v3) |
| Serial Number | Unique identifier issued by the CA |
| Subject | Entity the certificate identifies (CN=Common Name, O=Organization) |
| Issuer | CA that signed the certificate |
| Validity | Not Before / Not After dates |
| Public Key | Subject's public key and algorithm |
| Signature Algorithm | Algorithm used by the issuer to sign (e.g., SHA256withRSA) |
| Subject Alternative Names (SAN) | Additional hostnames/IPs the certificate covers |
| Basic Constraints | Whether this is a CA certificate |
| Key Usage | Permitted cryptographic operations |

### Why Root CA is Typically Not Sent

- The root CA certificate is already in the client's trust store
- Sending it wastes bandwidth and provides no security benefit
- The client must trust the root independently — receiving it over the network does not establish trust

## ServerKeyExchange Message (TLS 1.2)

Present when the selected cipher suite requires additional key exchange parameters:

| Cipher Suite Type | ServerKeyExchange | Parameters |
|-------------------|-------------------|------------|
| RSA | Not sent | Client encrypts pre-master secret with server's RSA public key |
| DHE_RSA | Sent | DH group parameters (p, g) and server's DH public value |
| ECDHE_RSA | Sent | Named curve and server's ECDH public point |
| ECDHE_ECDSA | Sent | Named curve and server's ECDH public point |

The parameters are signed with the server's private key to prevent man-in-the-middle attacks.

## ClientKeyExchange Message (TLS 1.2)

| Cipher Suite Type | Contents |
|-------------------|----------|
| RSA | Pre-master secret encrypted with server's public key |
| DHE / ECDHE | Client's DH/ECDH public value |

## Key Derivation

### TLS 1.2

```
Pre-Master Secret
       │
       ▼  (PRF with client_random + server_random)
Master Secret (48 bytes)
       │
       ▼  (PRF with client_random + server_random)
Key Material → client_write_MAC_key
             → server_write_MAC_key
             → client_write_key
             → server_write_key
             → client_write_IV
             → server_write_IV
```

### TLS 1.3

Uses HKDF (HMAC-based Key Derivation Function):
```
(EC)DHE Shared Secret
       │
       ▼  HKDF-Extract
Handshake Secret
       │
       ▼  Derive-Secret → handshake traffic keys
       │
       ▼  HKDF-Extract
Master Secret
       │
       ▼  Derive-Secret → application traffic keys
                        → resumption master secret
```

## ChangeCipherSpec (TLS 1.2)

A single-byte message (value 1) that signals:
- "All subsequent records from me will be encrypted with the negotiated keys"

Both client and server send this:
1. Client sends ChangeCipherSpec → Client sends Finished (encrypted)
2. Server sends ChangeCipherSpec → Server sends Finished (encrypted)

In TLS 1.3, ChangeCipherSpec is formally removed but may be sent as a compatibility measure (middlebox compatibility mode). It carries no cryptographic meaning in TLS 1.3.

## Finished Message

Contains a **verify_data** field: a hash of all previous handshake messages, computed with the negotiated keys.

- Proves both sides derived the same keys
- Confirms handshake integrity (no tampering)
- First encrypted message in TLS 1.2; follows encrypted messages in TLS 1.3

## Alert Protocol

Used to signal errors or connection closure:

| Level | Value | Description |
|-------|-------|-------------|
| Warning | 1 | Non-fatal alert |
| Fatal | 2 | Connection must be terminated |

### Common Alert Types

| Alert | Value | Description |
|-------|-------|-------------|
| close_notify | 0 | Graceful connection closure |
| unexpected_message | 10 | Received inappropriate message |
| bad_record_mac | 20 | Record MAC verification failed |
| handshake_failure | 40 | Unable to negotiate acceptable parameters |
| certificate_expired | 45 | Certificate has expired |
| unknown_ca | 48 | Certificate signed by unknown CA |

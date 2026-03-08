# TLS Protocol Overview

## What is TLS?

Transport Layer Security (TLS) provides secure communication over a computer network. It sits between the application layer (e.g., HTTP) and the transport layer (TCP), providing:

1. **Confidentiality**: Encryption of application data
2. **Integrity**: MAC (Message Authentication Code) protection against tampering
3. **Authentication**: Server (and optionally client) identity verification via certificates

## TLS Protocol Stack

```
┌─────────────────────────────────────────────┐
│           Application Protocol              │
│          (HTTP, SMTP, IMAP, etc.)           │
├─────────────────────────────────────────────┤
│  Handshake │ Change   │ Alert  │ Application│
│  Protocol  │ Cipher   │Protocol│ Data       │
│            │ Spec     │        │ Protocol   │
├─────────────────────────────────────────────┤
│              TLS Record Protocol             │
├─────────────────────────────────────────────┤
│                    TCP                       │
└─────────────────────────────────────────────┘
```

## TLS Record Protocol

The record protocol is the foundation layer. Every TLS message is wrapped in a record:

```
┌──────────────┬──────────────┬──────────────┬──────────────────────┐
│ Content Type │   Version    │    Length     │     Fragment         │
│   (1 byte)   │  (2 bytes)   │  (2 bytes)   │   (≤ 16384 bytes)   │
└──────────────┴──────────────┴──────────────┴──────────────────────┘
```

### Content Types

| Value | Type | Description |
|-------|------|-------------|
| 20 | ChangeCipherSpec | Signals transition to encrypted communication |
| 21 | Alert | Warning or fatal error notifications |
| 22 | Handshake | Key negotiation and authentication messages |
| 23 | Application Data | Encrypted application payload |

### Version Values

| Value | Version |
|-------|---------|
| 0x0301 | TLS 1.0 |
| 0x0302 | TLS 1.1 |
| 0x0303 | TLS 1.2 |
| 0x0303 | TLS 1.3 (record layer says 1.2 for compatibility) |

Note: TLS 1.3 uses 0x0303 in the record layer for backwards compatibility. The actual version is negotiated via the `supported_versions` extension.

## TLS 1.2 Handshake Flow

```
Client                                          Server
  │                                                │
  │──── ClientHello ─────────────────────────────→ │
  │                                                │
  │←─── ServerHello ──────────────────────────────│
  │←─── Certificate ──────────────────────────────│
  │←─── ServerKeyExchange (if needed) ────────────│
  │←─── ServerHelloDone ─────────────────────────│
  │                                                │
  │──── ClientKeyExchange ───────────────────────→ │
  │──── ChangeCipherSpec ────────────────────────→ │
  │──── Finished (encrypted) ────────────────────→ │
  │                                                │
  │←─── ChangeCipherSpec ─────────────────────────│
  │←─── Finished (encrypted) ────────────────────│
  │                                                │
  │←──→ Application Data (encrypted) ←──────────→ │
```

**Total: 2 round trips** before application data (not counting TCP handshake).

## TLS 1.3 Handshake Flow

```
Client                                          Server
  │                                                │
  │──── ClientHello + KeyShare ──────────────────→ │
  │                                                │
  │←─── ServerHello + KeyShare ───────────────────│
  │←─── {EncryptedExtensions} ────────────────────│
  │←─── {Certificate} ───────────────────────────│
  │←─── {CertificateVerify} ─────────────────────│
  │←─── {Finished} ──────────────────────────────│
  │                                                │
  │──── {Finished} ──────────────────────────────→ │
  │                                                │
  │←──→ Application Data (encrypted) ←──────────→ │
```

**Total: 1 round trip** (1-RTT). Messages in `{}` are encrypted.

### Key TLS 1.3 Improvements

1. **Fewer round trips**: 1-RTT handshake (vs 2-RTT in TLS 1.2)
2. **0-RTT resumption**: Clients can send data in the first flight using cached keys
3. **No ChangeCipherSpec**: Removed (may still be sent for middlebox compatibility)
4. **Encrypted handshake**: Certificate and extensions are encrypted after ServerHello
5. **Removed insecure algorithms**: No RSA key exchange, no CBC mode, no RC4, no SHA-1

## SSL vs TLS Naming

| Name | Version | Status |
|------|---------|--------|
| SSL 2.0 | — | Deprecated (insecure) |
| SSL 3.0 | — | Deprecated (POODLE attack) |
| TLS 1.0 | RFC 2246 | Deprecated |
| TLS 1.1 | RFC 4346 | Deprecated |
| TLS 1.2 | RFC 5246 | Current (widely used) |
| TLS 1.3 | RFC 8446 | Current (recommended) |

Wireshark still uses "SSL" in some filter names for backwards compatibility (e.g., `ssl` as an alias for `tls`).

## Cipher Suite Format

### TLS 1.2 Cipher Suite Naming

```
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
 │    │     │        │   │   │    │
 │    │     │        │   │   │    └── PRF hash
 │    │     │        │   │   └─── AEAD mode
 │    │     │        │   └────── Key size
 │    │     │        └─────────── Symmetric cipher
 │    │     └──────────────────── Authentication
 │    └────────────────────────── Key exchange
 └─────────────────────────────── Protocol
```

### TLS 1.3 Cipher Suite Naming (Simplified)

```
TLS_AES_128_GCM_SHA256
 │    │   │   │    │
 │    │   │   │    └── Hash for HKDF
 │    │   │   └─── AEAD mode
 │    │   └────── Key size
 │    └─────────── Symmetric cipher
 └──────────────── Protocol
```

TLS 1.3 separates key exchange from cipher suites — key exchange is negotiated via extensions (`key_share`, `supported_groups`).

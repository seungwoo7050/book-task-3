# Wireless Management Frames

## Overview

Management frames handle the establishment and maintenance of wireless connections. They are always sent unencrypted (even in WPA2 networks, unless 802.11w Protected Management Frames is used) and are identified by Type=00 in the Frame Control field.

## Beacon Frames (Subtype 0x08)

Beacon frames are periodically broadcast by Access Points to announce their presence and capabilities.

### Beacon Frame Body

| Field | Size | Description |
|-------|------|-------------|
| Timestamp | 8 bytes | AP's TSF (Timing Synchronization Function) timer value |
| Beacon Interval | 2 bytes | Time between beacons (typically 100 TU = 102.4 ms) |
| Capability Information | 2 bytes | Network capabilities (ESS, IBSS, privacy, etc.) |

### Common Information Elements in Beacons

| Element ID | Name | Description |
|-----------|------|-------------|
| 0 | SSID | Network name (0–32 bytes; length 0 = hidden SSID) |
| 1 | Supported Rates | Mandatory data rates (up to 8 rates) |
| 3 | DS Parameter Set | Current channel number |
| 5 | TIM | Traffic Indication Map for power-save clients |
| 48 | RSN (Robust Security Network) | WPA2 security parameters |
| 50 | Extended Supported Rates | Additional data rates beyond 8 |
| 221 | Vendor Specific | WPA (Microsoft OUI) and other vendor extensions |

### Beacon Interval

- 1 Time Unit (TU) = 1024 microseconds
- Default beacon interval = 100 TU ≈ 102.4 ms
- Approximately 10 beacons per second per AP

### Capability Information Bits

| Bit | Name | Description |
|-----|------|-------------|
| 0 | ESS | Extended Service Set (infrastructure mode) |
| 1 | IBSS | Independent BSS (ad-hoc mode) |
| 4 | Privacy | Encryption required (WEP/WPA/WPA2) |
| 5 | Short Preamble | Short preamble supported |
| 10 | Short Slot Time | Short slot time (9μs vs 20μs) used |

## Probe Request (Subtype 0x04)

Sent by a station to actively discover networks.

### Probe Request Body

| Field | Description |
|-------|-------------|
| SSID | Target network name (empty = wildcard, discovers all networks) |
| Supported Rates | Rates the station supports |

### Addressing

- **Destination**: `ff:ff:ff:ff:ff:ff` (broadcast) for wildcard probes
- **Source**: Station's MAC address
- **BSSID**: `ff:ff:ff:ff:ff:ff` (broadcast) for wildcard probes

## Probe Response (Subtype 0x05)

Sent by an AP in response to a probe request. Contains essentially the same information as a beacon frame.

### Key Differences from Beacons

- Unicast (directed to the requesting station), not broadcast
- Sent on demand rather than periodically
- Does not contain TIM (Traffic Indication Map)
- Otherwise contains the same information elements

## Authentication (Subtype 0x0b)

The authentication process in 802.11:

### Open System Authentication (most common)

```
Station                          AP
   │                              │
   │── Authentication Request ──→ │  (Algorithm=Open System, Seq=1)
   │                              │
   │←── Authentication Response ──│  (Algorithm=Open System, Seq=2, Status=Success)
   │                              │
```

### Authentication Frame Body

| Field | Size | Description |
|-------|------|-------------|
| Authentication Algorithm | 2 bytes | 0=Open System, 1=Shared Key |
| Authentication Sequence | 2 bytes | Transaction sequence number |
| Status Code | 2 bytes | 0=Success, others=failure reason |

### Status Codes

| Code | Meaning |
|------|---------|
| 0 | Successful |
| 1 | Unspecified failure |
| 12 | Association denied — reason outside scope of standard |
| 13 | Algorithm not supported |

## Association Request (Subtype 0x00)

Sent by a station after successful authentication to join the BSS.

### Association Request Body

| Field | Description |
|-------|-------------|
| Capability Information | Station's capabilities |
| Listen Interval | How often the station wakes to listen for buffered frames |
| SSID | Network the station wants to join |
| Supported Rates | Station's supported data rates |

## Association Response (Subtype 0x01)

AP's reply to an association request.

### Association Response Body

| Field | Description |
|-------|-------------|
| Capability Information | AP's capabilities |
| Status Code | Success/failure |
| Association ID (AID) | Unique ID assigned to the station (1–2007) |
| Supported Rates | AP's supported rates |

## Complete Connection Sequence

The full process for a station joining an infrastructure BSS:

```
Station                              AP
   │                                  │
   │  1. Scanning (passive or active) │
   │                                  │
   │── 2. Probe Request ────────────→ │  (optional, active scan)
   │←── 3. Probe Response ───────────│
   │                                  │
   │── 4. Authentication Request ───→ │
   │←── 5. Authentication Response ──│
   │                                  │
   │── 6. Association Request ──────→ │
   │←── 7. Association Response ─────│
   │                                  │
   │  8. 802.1X / 4-Way Handshake    │  (WPA/WPA2 only)
   │                                  │
   │── 9. Data Frames ─────────────→ │
   │←── 10. Data Frames ────────────│
```

## Deauthentication and Disassociation

### Deauthentication (Subtype 0x0c)

- Terminates the authentication relationship
- Implicitly disassociates the station
- Contains a Reason Code explaining why

### Disassociation (Subtype 0x0a)

- Terminates only the association (authentication remains)
- Station must re-associate before sending data
- Contains a Reason Code

### Common Reason Codes

| Code | Meaning |
|------|---------|
| 1 | Unspecified reason |
| 2 | Previous authentication no longer valid |
| 3 | Station leaving (or has left) the BSS |
| 4 | Inactivity disassociation |
| 8 | Station leaving (or has left) the ESS |

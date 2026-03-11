# Wireshark Wireless Analysis Techniques

## Monitor Mode vs Managed Mode

### Managed Mode (Default)

- Standard capture mode on most operating systems
- Only sees data frames destined for/from the capturing station
- 802.11 headers are typically stripped; frames appear as Ethernet
- Cannot see management frames (beacons, probes, auth) or control frames (ACK, RTS/CTS)

### Monitor Mode

- Special capture mode that sees ALL 802.11 frames on a channel
- Full 802.11 headers are preserved (including Frame Control, Duration, all 4 address fields)
- Includes a radio header (Radiotap or PPI) with signal strength and other radio metadata
- Required for this lab's analysis

## Opening 802.11 Captures in Wireshark

When opening a monitor-mode capture, Wireshark automatically detects the link-layer header type:

- **Radiotap**: Most common on Linux and macOS
- **PPI (Per-Packet Information)**: Alternative format
- **IEEE 802.11**: Raw 802.11 without radio metadata

## Essential Display Filters

### By Frame Type

```
wlan.fc.type == 0          # Management frames
wlan.fc.type == 1          # Control frames
wlan.fc.type == 2          # Data frames
```

### By Subtype

```
wlan.fc.type_subtype == 0x08    # Beacon
wlan.fc.type_subtype == 0x04    # Probe Request
wlan.fc.type_subtype == 0x05    # Probe Response
wlan.fc.type_subtype == 0x0b    # Authentication
wlan.fc.type_subtype == 0x00    # Association Request
wlan.fc.type_subtype == 0x01    # Association Response
wlan.fc.type_subtype == 0x1d    # ACK
wlan.fc.type_subtype == 0x1b    # RTS
wlan.fc.type_subtype == 0x1c    # CTS
```

### By Address

```
wlan.addr == aa:bb:cc:dd:ee:ff          # Any address field matches
wlan.sa == aa:bb:cc:dd:ee:ff            # Source address
wlan.da == aa:bb:cc:dd:ee:ff            # Destination address
wlan.bssid == aa:bb:cc:dd:ee:ff         # BSSID
wlan.ra == aa:bb:cc:dd:ee:ff            # Receiver address
wlan.ta == aa:bb:cc:dd:ee:ff            # Transmitter address
```

### By SSID

```
wlan.ssid == "MyNetwork"                # Exact SSID match
wlan.ssid contains "Net"                # SSID contains substring
```

### By Flags

```
wlan.fc.tods == 1                       # To Distribution System
wlan.fc.fromds == 1                     # From Distribution System
wlan.fc.retry == 1                      # Retransmitted frame
wlan.fc.protected == 1                  # Protected (encrypted) frame
```

### Combination Filters

```
# Beacons from a specific AP
wlan.fc.type_subtype == 0x08 && wlan.sa == aa:bb:cc:dd:ee:ff

# All management frames for a specific BSSID
wlan.fc.type == 0 && wlan.bssid == aa:bb:cc:dd:ee:ff

# Data frames between two stations
wlan.fc.type == 2 && wlan.sa == aa:bb:cc:dd:ee:ff && wlan.da == 11:22:33:44:55:66

# Authentication and association sequence
wlan.fc.type_subtype == 0x0b || wlan.fc.type_subtype == 0x00 || wlan.fc.type_subtype == 0x01
```

## Useful Wireshark Features for 802.11

### Wireless Toolbar

- **View → Wireless Toolbar**: Shows channel and signal information
- Only available on monitor-mode captures

### WLAN Statistics

- **Wireless → WLAN Traffic**: Summary of all BSSs detected
  - Lists APs by BSSID, SSID, channel, number of stations
  - Shows frame counts per BSS

### Decryption

- **Edit → Preferences → Protocols → IEEE 802.11**
  - Enable decryption and add WEP/WPA keys
  - Allows inspection of encrypted data frame payloads

### Coloring Rules

Wireshark applies default coloring:
- **Gray background**: Management frames
- **Pink/Light red**: Control frames
- Default colors vary by Wireshark version

## tshark Commands for 802.11 Analysis

### List All SSIDs

```bash
tshark -r capture.pcap -Y "wlan.fc.type_subtype == 0x08" \
    -T fields -e wlan.ssid | sort -u
```

### Frame Type Distribution

```bash
tshark -r capture.pcap -T fields -e wlan.fc.type_subtype | \
    sort | uniq -c | sort -rn
```

### Extract Beacon Interval

```bash
tshark -r capture.pcap -Y "wlan.fc.type_subtype == 0x08" \
    -T fields -e wlan.ssid -e wlan.fixed.beacon | head -20
```

### Track Association Sequence

```bash
tshark -r capture.pcap \
    -Y "wlan.fc.type_subtype == 0x04 || wlan.fc.type_subtype == 0x05 || \
        wlan.fc.type_subtype == 0x0b || wlan.fc.type_subtype == 0x00 || \
        wlan.fc.type_subtype == 0x01" \
    -T fields -e frame.number -e frame.time_relative \
    -e wlan.fc.type_subtype -e wlan.sa -e wlan.da
```

### Examine Duration Field

```bash
tshark -r capture.pcap -Y "wlan.fc.type == 2" \
    -T fields -e frame.number -e wlan.duration -e frame.len | head -20
```

## Radiotap Header Information

Monitor-mode captures include radio-layer metadata:

| Field | Description |
|-------|-------------|
| `radiotap.channel.freq` | Channel frequency (e.g., 2437 MHz = Channel 6) |
| `radiotap.dbm_antsignal` | Signal strength in dBm |
| `radiotap.datarate` | Data rate in Mbps |
| `radiotap.channel.flags` | Channel flags (band, modulation) |

### Channel to Frequency Mapping (2.4 GHz)

| Channel | Frequency (MHz) |
|---------|-----------------|
| 1 | 2412 |
| 6 | 2437 |
| 11 | 2462 |

## Troubleshooting

### "No 802.11 fields visible"
- Capture was likely in managed mode, not monitor mode
- Frames appear as Ethernet, not 802.11
- Re-capture in monitor mode

### "Encrypted data, cannot decode"
- Add decryption keys: Edit → Preferences → Protocols → IEEE 802.11
- For WPA2: Need the passphrase AND must have captured the 4-way handshake

### "Only seeing beacons, no data"
- The capture channel may not match the AP's data channel
- Lock the capture to the correct channel

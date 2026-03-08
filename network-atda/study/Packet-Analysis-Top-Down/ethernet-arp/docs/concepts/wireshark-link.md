# Wireshark Link Layer Analysis Techniques

## Display Filters for Ethernet

| Filter | Description |
| :--- | :--- |
| `eth` | All Ethernet frames |
| `eth.dst == ff:ff:ff:ff:ff:ff` | Broadcast frames |
| `eth.src == aa:bb:cc:dd:ee:ff` | Frames from a specific MAC |
| `eth.dst == aa:bb:cc:dd:ee:ff` | Frames to a specific MAC |
| `eth.addr == aa:bb:cc:dd:ee:ff` | Frames to or from a specific MAC |
| `eth.type == 0x0800` | Frames carrying IPv4 |
| `eth.type == 0x0806` | Frames carrying ARP |
| `eth.type == 0x86dd` | Frames carrying IPv6 |

## Display Filters for ARP

| Filter | Description |
| :--- | :--- |
| `arp` | All ARP traffic |
| `arp.opcode == 1` | ARP requests only |
| `arp.opcode == 2` | ARP replies only |
| `arp.src.proto_ipv4 == 192.168.1.1` | ARP from a specific IP |
| `arp.dst.proto_ipv4 == 192.168.1.5` | ARP targeting a specific IP |
| `arp.src.hw_mac == aa:bb:cc:dd:ee:ff` | ARP from a specific MAC |

## Analyzing Ethernet Frames

### Reading Frame Details

In Wireshark, the bottom layer (first in the packet details) shows the Ethernet header:

```
Ethernet II, Src: Dell_ab:cd:ef (aa:bb:cc:dd:ee:ff), Dst: Broadcast (ff:ff:ff:ff:ff:ff)
    Destination: ff:ff:ff:ff:ff:ff
        Address: ff:ff:ff:ff:ff:ff
        .... ..1. .... .... .... .... = LG bit: Locally administered address
        .... ...1 .... .... .... .... = IG bit: Group address (multicast/broadcast)
    Source: aa:bb:cc:dd:ee:ff
        Address: aa:bb:cc:dd:ee:ff
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
    Type: ARP (0x0806)
```

### Identifying Broadcast vs Unicast

- **Broadcast**: `Dst: ff:ff:ff:ff:ff:ff` — the IG (Individual/Group) bit is 1
- **Unicast**: `Dst: <specific MAC>` — the IG bit is 0
- **Multicast**: `Dst: 01:xx:xx:xx:xx:xx` — IG bit is 1, but not all-ff

### Counting Header Bytes

| Component | Bytes |
| :--- | :--- |
| Ethernet header (Dst + Src + Type) | 14 bytes |
| IP header (minimum) | 20 bytes |
| TCP header (minimum) | 20 bytes |
| **Total before HTTP data** | **54 bytes** |

So the first byte of HTTP data (e.g., "G" in "GET") appears at byte offset 54 from the start of the Ethernet frame.

## Analyzing ARP Packets

### ARP Details in Wireshark

```
Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: aa:bb:cc:dd:ee:ff
    Sender IP address: 192.168.1.100
    Target MAC address: 00:00:00:00:00:00
    Target IP address: 192.168.1.1
```

### Key Observations

1. **ARP Request Target MAC**: Always `00:00:00:00:00:00` — the sender doesn't know it yet
2. **Ethernet Destination for Request**: `ff:ff:ff:ff:ff:ff` — broadcast so all hosts see it
3. **ARP Reply**: Contains the resolved MAC; sent unicast to the requester
4. **Ethernet Destination for Reply**: The requester's MAC — direct unicast delivery

## tshark Commands

```bash
# List all ARP packets with details
tshark -r trace.pcapng -Y "arp" -T fields \
    -e frame.number -e arp.opcode \
    -e arp.src.hw_mac -e arp.src.proto_ipv4 \
    -e arp.dst.hw_mac -e arp.dst.proto_ipv4

# Show Ethernet header info
tshark -r trace.pcapng -T fields \
    -e frame.number -e eth.src -e eth.dst -e eth.type | head -20

# Count broadcast frames
tshark -r trace.pcapng -Y "eth.dst == ff:ff:ff:ff:ff:ff" | wc -l
```

## Tips

1. **MAC manufacturer lookup**: Wireshark resolves the OUI (first 3 bytes) to a manufacturer name (e.g., `Dell_ab:cd:ef`)
2. **Frame bytes view**: The Packet Bytes pane shows raw hex + ASCII, useful for counting byte offsets
3. **ARP comes before IP**: If you clear the ARP cache, you'll see an ARP exchange immediately before the first IP packet to a local host
4. **Router MAC**: When sending to a non-local IP, the Ethernet destination is the **router's** MAC, not the final destination's MAC

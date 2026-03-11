# Wireshark IP & ICMP Analysis Techniques

## Display Filters for IP

| Filter | Description |
| :--- | :--- |
| `ip` | All IPv4 traffic |
| `ip.addr == 192.168.1.1` | Traffic to/from a specific IP |
| `ip.src == 192.168.1.1` | Traffic from a specific source |
| `ip.dst == 128.119.245.12` | Traffic to a specific destination |
| `ip.ttl == 1` | Datagrams with TTL = 1 |
| `ip.ttl < 10` | Datagrams with low TTL |
| `ip.id == 12345` | Datagrams with a specific Identification |
| `ip.flags.mf == 1` | Datagrams with More Fragments flag set |
| `ip.frag_offset > 0` | Non-first fragments |
| `ip.flags.mf == 1 || ip.frag_offset > 0` | All fragmented datagrams |
| `ip.proto == 1` | IP datagrams carrying ICMP |
| `ip.proto == 6` | IP datagrams carrying TCP |
| `ip.proto == 17` | IP datagrams carrying UDP |

## Display Filters for ICMP

| Filter | Description |
| :--- | :--- |
| `icmp` | All ICMP traffic |
| `icmp.type == 8` | Echo Request (ping) |
| `icmp.type == 0` | Echo Reply |
| `icmp.type == 11` | Time Exceeded (traceroute) |
| `icmp.type == 3` | Destination Unreachable |
| `icmp.type == 3 && icmp.code == 3` | Port Unreachable |
| `icmp.ident == 1234` | ICMP with specific Identifier |
| `icmp.seq == 1` | ICMP with specific Sequence Number |

## Analyzing IP Fragmentation in Wireshark

### Identifying Fragments

1. Filter: `ip.flags.mf == 1 || ip.frag_offset > 0`
2. All matching packets are IP fragments
3. Fragments sharing the same **Identification** value belong to the same original datagram

### Reading Fragment Fields

In the IP header details pane:

```
Internet Protocol Version 4
    ...
    Identification: 0x3039 (12345)
    Flags: 0x2000, More fragments
        0... .... .... .... = Reserved bit: Not set
        .0.. .... .... .... = Don't fragment: Not set
        ..1. .... .... .... = More fragments: Set
    Fragment Offset: 0
    ...
```

### Fragment Offset Calculation

The Fragment Offset field is in **8-byte units**. To get the byte offset:

$$\text{Byte Offset} = \text{Fragment Offset} \times 8$$

### Reassembly View

Wireshark automatically reassembles fragments. On the **last fragment** (MF=0), you'll see:

```
[Reassembled IPv4 (3980 bytes)]
    [Fragment count: 3]
    [Reassembled IPv4 length: 3980]
    [Reassembled IPv4 data: ...]
```

## Analyzing Traceroute

### Filter for Traceroute Traffic

```
icmp.type == 8 || icmp.type == 11 || icmp.type == 0
```

### Mapping the Path

1. Filter ICMP Echo Requests (`icmp.type == 8`) — these show increasing TTL values
2. Filter ICMP Time Exceeded (`icmp.type == 11`) — the source IP of each is a router
3. The final ICMP Echo Reply (`icmp.type == 0`) comes from the destination

### tshark Commands

```bash
# List all ICMP packets with TTL and type
tshark -r trace.pcapng -Y "icmp" -T fields \
    -e frame.number -e ip.src -e ip.dst -e ip.ttl -e icmp.type -e icmp.code

# List only Echo Requests with their TTL
tshark -r trace.pcapng -Y "icmp.type == 8" -T fields \
    -e frame.number -e ip.ttl -e ip.id

# List Time Exceeded replies (routers along the path)
tshark -r trace.pcapng -Y "icmp.type == 11" -T fields \
    -e frame.number -e ip.src -e ip.ttl

# List fragments
tshark -r trace.pcapng -Y "ip.flags.mf == 1 || ip.frag_offset > 0" -T fields \
    -e frame.number -e ip.id -e ip.flags.mf -e ip.frag_offset -e ip.len
```

## Tips

1. **Relative vs Absolute**: Wireshark shows IP fields as-is (no relative numbering like TCP seq)
2. **Checksum recalculation**: Wireshark may show `[Header checksum: validation disabled]` — this is normal when capture offloading is enabled
3. **DF flag**: The Don't Fragment flag prevents routers from fragmenting; if the datagram is too large, the router drops it and sends ICMP Type 3, Code 4 (Fragmentation Needed)
4. **TTL values**: Common initial TTLs — Linux: 64, Windows: 128, Cisco routers: 255

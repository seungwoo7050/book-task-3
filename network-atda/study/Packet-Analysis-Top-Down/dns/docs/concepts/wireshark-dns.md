# Wireshark DNS Analysis Techniques

## Display Filters for DNS

### Basic Filters

| Filter | Description |
| :--- | :--- |
| `dns` | All DNS traffic |
| `dns.flags.response == 0` | Only DNS queries |
| `dns.flags.response == 1` | Only DNS responses |
| `dns.qry.name == "www.example.com"` | Queries for a specific domain |
| `dns.qry.type == 1` | A record queries only |
| `dns.qry.type == 28` | AAAA record queries only |
| `dns.qry.type == 5` | CNAME record queries only |
| `dns.qry.type == 2` | NS record queries only |
| `dns.qry.type == 15` | MX record queries only |

### Response Filters

| Filter | Description |
| :--- | :--- |
| `dns.flags.rcode == 0` | Successful responses (No Error) |
| `dns.flags.rcode == 3` | Name Error (NXDOMAIN) |
| `dns.flags.authoritative == 1` | Authoritative responses only |
| `dns.resp.ttl < 60` | Responses with TTL less than 60 seconds |
| `dns.a` | Responses containing A records |
| `dns.aaaa` | Responses containing AAAA records |
| `dns.cname` | Responses containing CNAME records |

### Combining Filters

```
dns.qry.name contains "example" && dns.flags.response == 1
dns.flags.response == 1 && dns.count.answers > 0
dns && ip.dst == 8.8.8.8
```

## Wireshark DNS Packet Details

When you select a DNS packet in Wireshark and expand the **Domain Name System** layer, you see:

### Query Example

```
Domain Name System (query)
    Transaction ID: 0xa1b2
    Flags: 0x0100 Standard query
        0... .... .... .... = Response: Message is a query
        .000 0... .... .... = Opcode: Standard query (0)
        .... ..0. .... .... = Truncated: Message is not truncated
        .... ...1 .... .... = Recursion desired: Do query recursively
    Questions: 1
    Answer RRs: 0
    Authority RRs: 0
    Additional RRs: 0
    Queries
        www.example.com: type A, class IN
            Name: www.example.com
            [Name Length: 15]
            Type: A (Host Address) (1)
            Class: IN (0x0001)
```

### Response Example

```
Domain Name System (response)
    Transaction ID: 0xa1b2
    Flags: 0x8180 Standard query response, No error
        1... .... .... .... = Response: Message is a response
        .... .0.. .... .... = Authoritative: Server is not an authority
        .... .... 1... .... = Recursion available: Server can do recursive queries
        .... .... .... 0000 = Reply code: No error (0)
    Questions: 1
    Answer RRs: 1
    Queries
        www.example.com: type A, class IN
    Answers
        www.example.com: type A, class IN, addr 93.184.216.34
            Name: www.example.com
            Type: A (Host Address) (1)
            Class: IN (0x0001)
            Time to live: 300 (5 minutes)
            Data length: 4
            Address: 93.184.216.34
```

## tshark Commands for DNS Analysis

### List All DNS Queries

```bash
tshark -r dns-trace.pcapng -Y "dns.flags.response == 0" -T fields \
    -e frame.number -e ip.dst -e dns.qry.name -e dns.qry.type
```

### List All DNS Responses with Answers

```bash
tshark -r dns-trace.pcapng -Y "dns.flags.response == 1" -T fields \
    -e frame.number -e dns.qry.name -e dns.a -e dns.aaaa -e dns.cname -e dns.resp.ttl
```

### Query-Response Matching

DNS queries and responses are matched by Transaction ID. To correlate them:

```bash
tshark -r dns-trace.pcapng -Y "dns" -T fields \
    -e frame.number -e dns.id -e dns.flags.response -e dns.qry.name
```

Look for matching `dns.id` values between queries (response=0) and responses (response=1).

## Tips for This Lab

1. **Port identification**: DNS uses UDP port 53 — verify in the UDP header
2. **Local resolver**: Your DNS queries go to your configured local resolver (check `ip.dst`)
3. **Record type numbers**: A=1, NS=2, CNAME=5, MX=15, AAAA=28
4. **TTL countdown**: If you query the same name twice, the second response may show a lower TTL (cache-served)
5. **CNAME chains**: A CNAME response points to another name, which may require a separate A record lookup

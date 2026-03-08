# DNS Hierarchy and Resolution

## The DNS Hierarchy

DNS is organized as a **distributed, hierarchical** database. No single server holds all DNS records. Instead, the namespace is divided into zones managed by different organizations.

```
                    . (Root)
                   / | \
                com  org  edu  net  ...     ← Top-Level Domains (TLD)
               / |        |
          google  example  mit              ← Second-Level Domains
           /
         www                                ← Hostnames
```

### Server Types

| Server Type | Role | Example |
| :--- | :--- | :--- |
| **Root DNS Server** | Knows the addresses of all TLD servers | `a.root-servers.net` (13 root server clusters) |
| **TLD DNS Server** | Knows the authoritative servers for domains under its TLD | `a.gtld-servers.net` (for .com) |
| **Authoritative DNS Server** | Holds the actual DNS records for a domain | `ns1.google.com` (for google.com) |
| **Local DNS Server (Resolver)** | Acts as a proxy, performing recursive resolution for clients | `8.8.8.8` (Google Public DNS) |

## Resolution Process

### Recursive Query

The client asks its **local DNS resolver** to do all the work:

```
1. Client → Local Resolver:  "What is the IP for www.example.com?"
2. Local Resolver → Root Server:  "Who handles .com?"
3. Root Server → Local Resolver:  "Ask a.gtld-servers.net"
4. Local Resolver → TLD Server:  "Who handles example.com?"
5. TLD Server → Local Resolver:  "Ask ns1.example.com"
6. Local Resolver → Authoritative:  "What is the IP for www.example.com?"
7. Authoritative → Local Resolver:  "93.184.216.34, TTL=300"
8. Local Resolver → Client:  "93.184.216.34"
```

### Iterative Query

The server does not resolve the query itself; instead, it returns a referral:

```
Client → Server: "What is www.example.com?"
Server → Client: "I don't know, but ask THIS server"   (referral)
```

In practice, **clients issue recursive queries** to their local resolver, and the **local resolver uses iterative queries** to walk the hierarchy.

## DNS Caching

### How It Works

Every DNS record has a **TTL (Time to Live)** value in seconds. When a resolver receives a record, it caches the record for that duration:

1. First query for `www.example.com` → resolver contacts root → TLD → authoritative
2. Response includes `TTL: 300` (5 minutes)
3. Subsequent queries within 5 minutes → resolver answers from cache immediately
4. After 5 minutes → cache entry expires → resolver must query again

### TTL in Wireshark

In a DNS response, each resource record shows its TTL:

```
www.example.com: type A, class IN, addr 93.184.216.34
    Name: www.example.com
    Type: A (Host Address) (1)
    Class: IN (0x0001)
    Time to live: 300 (5 minutes)
    Data length: 4
    Address: 93.184.216.34
```

If you query the same name twice and the second response has a **lower TTL**, it means the resolver served it from cache (the TTL counts down from the original value).

### Cache Effect on Latency

| Scenario | Latency |
| :--- | :--- |
| Cold cache (first query) | 50–200 ms (multiple round trips) |
| Warm cache (cached) | < 1 ms (local lookup) |

## Authoritative vs Non-Authoritative Answers

| Property | Authoritative | Non-Authoritative |
| :--- | :--- | :--- |
| Source | The server that owns the zone | A caching resolver |
| AA flag | Set (`AA = 1`) | Not set (`AA = 0`) |
| Freshness | Always current | May be stale (within TTL) |
| Example | `ns1.example.com` answering for `example.com` | Google DNS (`8.8.8.8`) using cached data |

In Wireshark, check the **AA (Authoritative Answer)** flag in the DNS response header:
- `Authoritative: Answer` = The server is the authority for this domain
- Field: `dns.flags.authoritative == 1`

## Command-Line DNS Tools

### nslookup

```bash
# Basic A record query
nslookup www.example.com

# Query a specific DNS server
nslookup www.example.com 8.8.8.8

# Query for NS records
nslookup -type=NS example.com

# Query for MX records
nslookup -type=MX example.com
```

### dig

```bash
# Basic A record query
dig www.example.com

# Query for specific record type
dig www.example.com AAAA

# Query a specific server
dig @8.8.8.8 www.example.com

# Trace the full resolution path
dig +trace www.example.com
```

Both tools generate DNS query packets that you can capture with Wireshark.

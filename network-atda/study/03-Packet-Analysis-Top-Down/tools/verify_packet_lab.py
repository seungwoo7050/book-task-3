#!/usr/bin/env python3
"""Stronger answer verification for Packet Analysis Top-Down labs.

This validator does two things:
1. Checks that the expected question headings exist.
2. Derives key facts from the provided traces with tshark and verifies that the
   public answer document actually mentions those facts.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path


QUESTION_COUNTS = {
    "http": 19,
    "dns": 16,
    "tcp-udp": 21,
    "ip-icmp": 18,
    "ethernet-arp": 17,
    "wireless-802.11": 18,
    "tls-ssl": 20,
    "http2-quic": 12,
}


class ValidationError(Exception):
    pass


class Validator:
    def __init__(self, text: str) -> None:
        self.text = text
        self.failures: list[str] = []

    def require_regex(self, label: str, pattern: str, flags: int = re.IGNORECASE | re.MULTILINE) -> None:
        if re.search(pattern, self.text, flags) is None:
            self.failures.append(f"Missing or mismatched answer content: {label}")

    def require_literal(self, label: str, literal: str) -> None:
        self.require_regex(label, re.escape(literal))

    def require_any(self, label: str, patterns: list[str], flags: int = re.IGNORECASE | re.MULTILINE) -> None:
        if not any(re.search(pattern, self.text, flags) for pattern in patterns):
            self.failures.append(f"Missing or mismatched answer content: {label}")

    def require_question_count(self, expected: int) -> None:
        count = len(
            re.findall(
                r"^###\s+(?:Question\s+\d+|Q\d+\.)",
                self.text,
                re.MULTILINE,
            )
        )
        if count != expected:
            self.failures.append(f"Question heading count mismatch: expected {expected}, found {count}")


def run_tshark(trace: Path, fields: list[str], display_filter: str | None = None) -> list[dict[str, str]]:
    cmd = [
        "tshark",
        "-r",
        str(trace),
    ]
    if display_filter:
        cmd += ["-Y", display_filter]
    cmd += [
        "-T",
        "fields",
        "-E",
        "header=n",
        "-E",
        "separator=\t",
        "-E",
        "occurrence=f",
        "-E",
        "aggregator=,",
    ]
    for field in fields:
        cmd += ["-e", field]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    rows: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < len(fields):
            parts += [""] * (len(fields) - len(parts))
        rows.append(dict(zip(fields, parts)))
    return rows


def decode_ssid(value: str) -> str:
    if not value:
        return value
    if re.fullmatch(r"[0-9a-fA-F]+", value) and len(value) % 2 == 0:
        try:
            decoded = bytes.fromhex(value).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return value
        if decoded.isprintable():
            return decoded
    return value


def analysis_file_for(lab_dir: Path) -> Path:
    files = sorted((lab_dir / "analysis" / "src").glob("*.md"))
    if len(files) != 1:
        raise ValidationError(f"Expected exactly one analysis markdown file under {lab_dir / 'analysis' / 'src'}")
    return files[0]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def first(rows: list[dict[str, str]], predicate) -> dict[str, str]:
    for row in rows:
        if predicate(row):
            return row
    raise ValidationError("Failed to extract required trace row")


def verify_http(lab_dir: Path, validator: Validator) -> None:
    data_dir = lab_dir / "problem" / "data"
    fields = [
        "frame.number",
        "ip.src",
        "ip.dst",
        "http.request.method",
        "http.request.uri",
        "http.response.code",
        "http.response.phrase",
        "http.accept_language",
        "http.connection",
        "http.last_modified",
        "http.content_length_header",
        "http.request.line",
        "http.response.line",
        "http.referer",
        "tcp.len",
    ]

    basic = run_tshark(data_dir / "http-basic.pcapng", fields, "http || tcp")
    basic_request = first(basic, lambda row: row["http.request.method"] == "GET")
    basic_response = first(basic, lambda row: row["http.response.code"] == "200")

    conditional = run_tshark(data_dir / "http-conditional.pcapng", fields, "http || tcp")
    cond_requests = [row for row in conditional if row["http.request.method"] == "GET"]
    cond_first_response = first(conditional, lambda row: row["http.response.code"] == "200")
    cond_second_response = first(conditional, lambda row: row["http.response.code"] == "304")

    long_doc = run_tshark(data_dir / "http-long-document.pcapng", fields, "http || tcp")
    long_request = first(long_doc, lambda row: row["http.request.method"] == "GET")
    long_response = first(long_doc, lambda row: row["http.response.code"] == "200")
    long_segments = sum(
        1
        for row in long_doc
        if row["ip.src"] == long_response["ip.src"] and row["tcp.len"].isdigit() and int(row["tcp.len"]) > 0
    )

    embedded = run_tshark(data_dir / "http-embedded-objects.pcapng", fields, "http || tcp")
    embedded_requests = [row for row in embedded if row["http.request.method"] == "GET"]
    embedded_destinations = sorted({row["ip.dst"] for row in embedded_requests if row["ip.dst"]})
    embedded_referers = sorted({row["http.referer"] for row in embedded_requests if row["http.referer"]})

    validator.require_literal("basic client IP", basic_request["ip.src"])
    validator.require_literal("basic server IP", basic_request["ip.dst"])
    validator.require_literal("Accept-Language header", basic_request["http.accept_language"])
    validator.require_literal("Last-Modified header", basic_response["http.last_modified"])
    validator.require_regex("basic Content-Length", rf"\b{re.escape(basic_response['http.content_length_header'])}\s+bytes\b")
    validator.require_literal("Connection header", basic_response["http.connection"])
    validator.require_literal("conditional If-Modified-Since date", basic_response["http.last_modified"])
    validator.require_regex("conditional first response 200 OK", r"\b200 OK\b")
    validator.require_literal("conditional second response phrase", f"{cond_second_response['http.response.code']} {cond_second_response['http.response.phrase']}")
    validator.require_any(
        "long document GET count",
        [
            rf"HTTP GET requests?:\s*\*\*?1\*\*?",
            rf"\b1\b.*HTTP GET requests?",
        ],
    )
    validator.require_any(
        "long document segment count",
        [
            rf"segments?.*\*\*?{long_segments}\*\*?",
            rf"\b{long_segments}\b.*segments?",
        ],
    )
    validator.require_regex("long document content length", rf"Content-Length.*\b{re.escape(long_response['http.content_length_header'])}\b|\b{re.escape(long_response['http.content_length_header'])}\s+bytes\b")
    validator.require_any(
        "embedded GET count",
        [
            rf"\*\*?{len(embedded_requests)}\s+GET requests?\*\*?",
            rf"\*\*?{len(embedded_requests)}\*\*?\s+GET requests?",
            rf"GET requests?.*\*\*?{len(embedded_requests)}\*\*?",
        ],
    )
    for destination in embedded_destinations:
        validator.require_literal("embedded destination IP", destination)
    for referer in embedded_referers:
        validator.require_literal("embedded Referer", referer)
    for uri in [row["http.request.uri"] for row in embedded_requests]:
        validator.require_literal("embedded request URI", uri)
    validator.require_any("serial image download interpretation", [r"\bserially\b", r"\bno overlap\b"])

    # 첫 번째 conditional request는 validator가 없는 요청으로 설명되어야 한다.
    if "If-Modified-Since:" in cond_requests[0]["http.request.line"]:
        raise ValidationError("Unexpected trace shape: first conditional request already contains If-Modified-Since")
    validator.require_any(
        "first conditional request has no validators",
        [r"neither `?If-Modified-Since`? nor `?If-None-Match`?", r"no `?If-Modified-Since`?.*no `?If-None-Match`?"],
    )


def verify_dns(lab_dir: Path, validator: Validator) -> None:
    data_dir = lab_dir / "problem" / "data"
    fields = [
        "frame.number",
        "ip.dst",
        "dns.flags.authoritative",
        "dns.qry.name",
        "dns.qry.type",
        "dns.count.answers",
        "dns.resp.type",
        "dns.a",
        "dns.cname",
        "dns.resp.ttl",
        "_ws.col.Info",
    ]

    nslookup = run_tshark(data_dir / "dns-nslookup.pcapng", fields, "dns")
    browsing = run_tshark(data_dir / "dns-web-browsing.pcapng", fields, "dns")

    query_a = first(nslookup, lambda row: row["dns.qry.type"] == "1" and row["dns.count.answers"] == "0")
    query_mx = first(nslookup, lambda row: row["dns.qry.type"] == "15" and row["dns.count.answers"] == "0")
    response_a = first(nslookup, lambda row: row["dns.resp.type"] == "1")
    response_mx = first(nslookup, lambda row: "Malformed Packet" in row["_ws.col.Info"])
    browsing_query = first(browsing, lambda row: row["dns.count.answers"] == "0")
    browsing_response = first(browsing, lambda row: row["dns.cname"])

    validator.require_literal("DNS server IP", query_a["ip.dst"])
    validator.require_literal("DNS A query type", "A (1)")
    validator.require_literal("DNS MX query type", "MX (15)")
    validator.require_literal("A response IP address", response_a["dns.a"])
    validator.require_literal("A response TTL", response_a["dns.resp.ttl"])
    validator.require_any("absence of example.com CNAME", [r"\bno CNAME\b", r"there is \*\*no CNAME\*\*"])
    validator.require_literal("malformed MX response note", "Malformed Packet: DNS")
    validator.require_literal("authoritative response flag", "Authoritative: 1")
    validator.require_literal("non-authoritative response flag", "Authoritative: 0")
    validator.require_literal("browsing DNS server IP", browsing_query["ip.dst"])
    validator.require_literal("browsing CNAME target", browsing_response["dns.cname"])
    validator.require_literal("browsing TTL", browsing_response["dns.resp.ttl"])
    validator.require_any("no TCP packets in browsing trace", [r"\bno TCP packets\b", r"`tcp` filter returns zero"])

    if query_mx["ip.dst"] != query_a["ip.dst"]:
        raise ValidationError("Unexpected trace shape: A and MX queries use different resolvers")


def verify_tcp_udp(lab_dir: Path, validator: Validator) -> None:
    data_dir = lab_dir / "problem" / "data"
    tcp_fields = [
        "frame.number",
        "ip.src",
        "tcp.srcport",
        "ip.dst",
        "tcp.dstport",
        "tcp.seq",
        "tcp.ack",
        "tcp.len",
        "tcp.window_size_value",
        "http.request.method",
        "http.request.uri",
    ]
    udp_fields = [
        "frame.number",
        "udp.srcport",
        "udp.dstport",
        "udp.length",
        "ip.proto",
    ]

    tcp_rows = run_tshark(data_dir / "tcp-upload.pcapng", tcp_fields, "tcp || http")
    udp_rows = run_tshark(data_dir / "udp-dns.pcapng", udp_fields, "udp")
    retransmissions = run_tshark(data_dir / "tcp-upload.pcapng", ["frame.number"], "tcp.analysis.retransmission")
    fin_packets = run_tshark(data_dir / "tcp-upload.pcapng", ["frame.number"], "tcp.flags.fin == 1")

    client_syn = first(tcp_rows, lambda row: row["frame.number"] == "1")
    server_synack = first(tcp_rows, lambda row: row["frame.number"] == "2")
    post_row = first(tcp_rows, lambda row: row["http.request.method"] == "POST")
    client_data_bytes = sum(int(row["tcp.len"]) for row in tcp_rows if row["ip.src"] == client_syn["ip.src"] and row["tcp.len"].isdigit())
    query = first(udp_rows, lambda row: row["frame.number"] == "1")
    response = first(udp_rows, lambda row: row["frame.number"] == "2")

    validator.require_literal("TCP client endpoint", f"{client_syn['ip.src']}:{client_syn['tcp.srcport']}")
    validator.require_literal("TCP server endpoint", f"{client_syn['ip.dst']}:{client_syn['tcp.dstport']}")
    validator.require_literal("SYN-ACK sequence number", f"`tcp.seq = {server_synack['tcp.seq']}`")
    validator.require_literal("SYN-ACK acknowledgment number", f"`tcp.ack = {server_synack['tcp.ack']}`")
    validator.require_literal("POST URI", post_row["http.request.uri"])
    validator.require_literal("POST sequence number", f"`tcp.seq = {post_row['tcp.seq']}`")
    validator.require_literal("POST acknowledgment number", f"`tcp.ack = {post_row['tcp.ack']}`")
    validator.require_regex("total client bytes", rf"\b{client_data_bytes}\s+bytes\b")
    validator.require_any("no retransmissions", [r"\bNo retransmissions observed\b", r"`tcp\.analysis\.retransmission` returns no matching frames"])
    validator.require_any("no FIN teardown in trace", [r"\bNo FIN packets are present\b", r"\bNot observable\b"])
    validator.require_literal("UDP query length", query["udp.length"])
    validator.require_literal("UDP maximum payload from length field", "65527")
    validator.require_literal("UDP maximum payload over IPv4", "65507")
    validator.require_literal("UDP protocol number", "17")
    validator.require_literal("TCP protocol number", "6")
    validator.require_literal("DNS query ports", f"{query['udp.srcport']} -> {query['udp.dstport']}")
    validator.require_literal("DNS response ports", f"{response['udp.srcport']} -> {response['udp.dstport']}")

    if retransmissions:
        raise ValidationError("Unexpected trace shape: retransmissions are present")
    if fin_packets:
        raise ValidationError("Unexpected trace shape: FIN packets are present")


def verify_ip_icmp(lab_dir: Path, validator: Validator) -> None:
    data_dir = lab_dir / "problem" / "data"
    fields = [
        "frame.number",
        "ip.src",
        "ip.dst",
        "ip.ttl",
        "ip.id",
        "ip.flags.mf",
        "ip.frag_offset",
        "ip.len",
        "ip.proto",
        "icmp.type",
        "icmp.code",
        "icmp.ident",
        "icmp.seq",
        "_ws.col.Info",
    ]

    traceroute = run_tshark(data_dir / "ip-traceroute.pcapng", fields, "ip || icmp")
    fragmentation = run_tshark(data_dir / "ip-fragmentation.pcapng", fields, "ip || icmp")

    first_request = first(traceroute, lambda row: row["frame.number"] == "1")
    router_rows = [row for row in traceroute if row["icmp.type"] == "11"]
    fragment_rows = [row for row in fragmentation if row["ip.id"] == "0x3039"]
    reply_row = first(traceroute, lambda row: row["icmp.type"] == "0")

    validator.require_literal("first request total length", first_request["ip.len"])
    validator.require_literal("first request ID", first_request["ip.id"])
    validator.require_literal("first request TTL", f"TTL: **{first_request['ip.ttl']}**")
    validator.require_literal("first request protocol number", "**1** (ICMP)")
    validator.require_literal("traceroute source IP", first_request["ip.src"])
    validator.require_literal("traceroute destination IP", first_request["ip.dst"])
    validator.require_literal("TTL increment pattern", "1 -> 2 -> 3")
    for row in router_rows:
        validator.require_literal("router hop source IP", row["ip.src"].split(",")[0])
    validator.require_literal("fragment datagram ID", "0x3039")
    validator.require_literal("middle fragment offset", fragment_rows[1]["ip.frag_offset"])
    validator.require_literal("last fragment offset", fragment_rows[2]["ip.frag_offset"])
    validator.require_literal("reassembled payload size", "3508")
    validator.require_literal("echo request type/code", "Type 8, Code 0")
    validator.require_literal("echo reply type/code", "Type 0, Code 0")
    validator.require_literal("time exceeded type/code", "Type 11, Code 0")
    validator.require_literal("ICMP identifier", reply_row["icmp.ident"])
    validator.require_literal("ICMP sequence number", reply_row["icmp.seq"])
    validator.require_literal("trace payload marker", "0x7472616365")


def verify_ethernet_arp(lab_dir: Path, validator: Validator) -> None:
    trace = lab_dir / "problem" / "data" / "ethernet-arp.pcapng"
    fields = [
        "frame.number",
        "eth.src",
        "eth.dst",
        "eth.type",
        "arp.opcode",
        "arp.src.hw_mac",
        "arp.src.proto_ipv4",
        "arp.dst.hw_mac",
        "arp.dst.proto_ipv4",
        "_ws.col.Info",
    ]
    rows = run_tshark(trace, fields)

    request = first(rows, lambda row: row["arp.opcode"] == "1")
    reply = first(rows, lambda row: row["arp.opcode"] == "2")
    ip_frame = first(rows, lambda row: row["eth.type"] == "0x0800")

    validator.require_literal("ARP request broadcast destination", request["eth.dst"])
    validator.require_literal("ARP request source MAC", request["eth.src"])
    validator.require_literal("ARP EtherType", request["eth.type"])
    validator.require_any("missing HTTP GET is called out", [r"\bNot observable\b", r"does not contain an HTTP GET"])
    validator.require_literal("ARP reply destination MAC", reply["eth.dst"])
    validator.require_literal("IPv4 EtherType", ip_frame["eth.type"])
    validator.require_literal("ARP sender IP", request["arp.src.proto_ipv4"])
    validator.require_literal("ARP target IP", request["arp.dst.proto_ipv4"])
    validator.require_literal("ARP unknown target MAC", request["arp.dst.hw_mac"])
    validator.require_literal("ARP reply sender MAC", reply["arp.src.hw_mac"])
    validator.require_literal("resolved MAC reused by IP frame", reply["arp.src.hw_mac"])
    validator.require_literal("request/reply/IP sequence frame #1", "frame #1")
    validator.require_literal("request/reply/IP sequence frame #2", "frame #2")
    validator.require_literal("request/reply/IP sequence frame #3", "frame #3")


def verify_wireless(lab_dir: Path, validator: Validator) -> None:
    trace = lab_dir / "problem" / "data" / "wireless-trace.pcap"
    fields = [
        "frame.number",
        "wlan.fc.type_subtype",
        "wlan.sa",
        "wlan.da",
        "wlan.ra",
        "wlan.ta",
        "wlan.bssid",
        "wlan.ssid",
        "wlan.fixed.beacon",
        "wlan.fixed.auth.alg",
        "wlan.fixed.status_code",
        "wlan.fixed.aid",
        "wlan.fixed.listen_ival",
        "wlan.fixed.capabilities",
        "wlan.fc.tods",
        "wlan.fc.fromds",
        "wlan.duration",
    ]
    rows = run_tshark(trace, fields)
    for row in rows:
        row["wlan.ssid"] = decode_ssid(row["wlan.ssid"])

    beacon_1 = first(rows, lambda row: row["frame.number"] == "1")
    beacon_2 = first(rows, lambda row: row["frame.number"] == "2")
    probe_request = first(rows, lambda row: row["frame.number"] == "3")
    auth_request = first(rows, lambda row: row["frame.number"] == "5")
    assoc_response = first(rows, lambda row: row["frame.number"] == "8")
    data_frame = first(rows, lambda row: row["frame.number"] == "9")
    ack_frame = first(rows, lambda row: row["frame.number"] == "10")

    validator.require_literal("beacon SSID #1", beacon_1["wlan.ssid"])
    validator.require_literal("beacon SSID #2", beacon_2["wlan.ssid"])
    validator.require_literal("beacon interval", f"{beacon_1['wlan.fixed.beacon']} TU")
    validator.require_literal("AP MAC/BSSID", beacon_1["wlan.sa"])
    validator.require_literal("probe request source MAC", probe_request["wlan.sa"])
    validator.require_literal("probe request broadcast destination", probe_request["wlan.da"])
    validator.require_any("open system auth", [r"\bOpen System\b", rf"Authentication Algorithm: {auth_request['wlan.fixed.auth.alg']}"])
    validator.require_literal("association success status", assoc_response["wlan.fixed.status_code"])
    validator.require_literal("association ID", assoc_response["wlan.fixed.aid"])
    validator.require_literal("data frame subtype", data_frame["wlan.fc.type_subtype"])
    validator.require_literal("To DS flag", f"To DS={1 if data_frame['wlan.fc.tods'] == 'True' else 0}")
    validator.require_literal("From DS flag", f"From DS={1 if data_frame['wlan.fc.fromds'] == 'True' else 0}")
    validator.require_literal("data frame duration", data_frame["wlan.duration"])
    validator.require_literal("ACK subtype", ack_frame["wlan.fc.type_subtype"])
    validator.require_literal("ACK receiver address", ack_frame["wlan.ra"])


def verify_tls(lab_dir: Path, validator: Validator) -> None:
    trace = lab_dir / "problem" / "data" / "tls-trace.pcap"
    fields = [
        "frame.number",
        "ip.src",
        "tcp.srcport",
        "ip.dst",
        "tcp.dstport",
        "tls.record.content_type",
        "tls.record.version",
        "tls.handshake.type",
        "tls.handshake.version",
        "tls.handshake.ciphersuite",
        "tls.handshake.extensions_server_name",
        "tls.change_cipher_spec",
        "tls.record.length",
        "tls.handshake.certificates_length",
        "tls.handshake.certificate_length",
        "_ws.col.Info",
    ]
    rows = run_tshark(trace, fields)

    client_hello = first(rows, lambda row: row["frame.number"] == "4")
    server_hello = first(rows, lambda row: row["frame.number"] == "5")
    ccs = first(rows, lambda row: row["frame.number"] == "6")

    validator.require_literal("ClientHello record version", client_hello["tls.record.version"])
    for suite in client_hello["tls.handshake.ciphersuite"].split(","):
        validator.require_literal("ClientHello cipher suite", suite)
    validator.require_any("missing SNI is called out", [r"\bSNI is \*\*not present\*\*", r"\bno `?server_name` extension\b"])
    validator.require_literal("ServerHello selected cipher suite", "0x1301")
    validator.require_literal("certificate list length", server_hello["tls.handshake.certificates_length"])
    validator.require_literal("certificate length", server_hello["tls.handshake.certificate_length"])
    validator.require_literal("malformed certificate note", "Malformed Packet: TLS")
    validator.require_literal("single CCS count", "Observed ChangeCipherSpec count: **1**")
    validator.require_literal("application data content type", "Content Type: **23**")
    validator.require_literal("application data length", "Length: **32**")
    validator.require_literal("TLS destination port", ccs["tcp.dstport"])
    validator.require_literal("application protocol hint", "Hypertext Transfer Protocol")
    validator.require_any("hybrid trace interpretation", [r"\bhybrid/minimal synthetic pattern\b", r"\bstrict 1\.2 vs 1\.3 comparison is limited\b"])


def verify_http2_quic(lab_dir: Path, validator: Validator) -> None:
    data_dir = lab_dir / "problem" / "data"
    http2_rows = read_tsv(data_dir / "http2-trace.tsv")
    quic_rows = read_tsv(data_dir / "quic-trace.tsv")

    http2_headers = [row for row in http2_rows if row["frame_type"] == "HEADERS"]
    http2_data = [row for row in http2_rows if row["frame_type"] == "DATA"]
    http2_window_update = first(http2_rows, lambda row: row["frame_type"] == "WINDOW_UPDATE")
    quic_client_rows = [row for row in quic_rows if row["endpoint"] == "client"]
    quic_server_rows = [row for row in quic_rows if row["endpoint"] == "server"]

    validator.require_literal("HTTP/2 transport", "TCP port 443")
    validator.require_literal("HTTP/2 ALPN", "`h2`")
    for row in http2_headers:
        validator.require_literal("HTTP/2 stream id", f"stream {row['stream_id']}")
        validator.require_literal("HTTP/2 frame number", f"Frame **{row['frame']}**")
    validator.require_literal("HTTP/2 interleaved DATA frame #1", f"frames **{http2_data[0]['frame']}**")
    validator.require_literal("HTTP/2 interleaved DATA frame #2", f"**{http2_data[1]['frame']}**")
    validator.require_literal("HTTP/2 flow-control frame", f"Frame **{http2_window_update['frame']}**")
    validator.require_literal("HTTP/2 WINDOW_UPDATE", "`WINDOW_UPDATE`")
    validator.require_literal("HTTP/2 HOL note", "head-of-line blocking")

    validator.require_literal("QUIC transport", "UDP port 443")
    for packet_type in ["Initial", "Handshake", "1-RTT"]:
        validator.require_literal("QUIC packet type", f"`{packet_type}`")
    validator.require_literal("QUIC client connection ID", quic_client_rows[0]["connection_id"])
    validator.require_literal("QUIC server connection ID", quic_server_rows[0]["connection_id"])
    validator.require_literal("QUIC stream 4", "stream **4**")
    validator.require_literal("QUIC stream 8", "stream **8**")
    validator.require_literal("QUIC control stream 0", "stream **0**")
    validator.require_literal("QUIC packet number sequence", "0, 1, 2, 3, 4")
    validator.require_any(
        "comparison mentions transport-level multiplexing",
        [r"transport-level multiplexing", r"moves multiplexing into the transport"],
    )


LAB_VERIFIERS = {
    "http": verify_http,
    "dns": verify_dns,
    "tcp-udp": verify_tcp_udp,
    "ip-icmp": verify_ip_icmp,
    "ethernet-arp": verify_ethernet_arp,
    "wireless-802.11": verify_wireless,
    "tls-ssl": verify_tls,
    "http2-quic": verify_http2_quic,
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_packet_lab.py <lab_dir>", file=sys.stderr)
        return 2

    lab_dir = Path(sys.argv[1]).resolve()
    lab_name = lab_dir.name
    if lab_name not in LAB_VERIFIERS:
        print(f"Unsupported lab: {lab_name}", file=sys.stderr)
        return 2

    try:
        answer_file = analysis_file_for(lab_dir)
        validator = Validator(answer_file.read_text(encoding="utf-8"))
        validator.require_question_count(QUESTION_COUNTS[lab_name])
        LAB_VERIFIERS[lab_name](lab_dir, validator)
    except FileNotFoundError as exc:
        print(f"FAIL: missing required file: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "(no stderr)"
        print(f"FAIL: tshark command failed: {stderr}", file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    if validator.failures:
        print(f"=== {lab_name} answer verification ===")
        for failure in validator.failures:
            print(f"- {failure}")
        return 1

    print(f"PASS: {lab_name} answer file passed content verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

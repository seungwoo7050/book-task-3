# 03. Packet Analysis Top-Down blog

HTTP에서 TLS를 지나 HTTP/2와 QUIC 비교까지 내려가며 Wireshark trace를 문제-증거-해설 구조로 읽는 단계입니다.

## 이 트랙에서 무엇을 따라가면 되나

이 레이어는 프로젝트를 나열하는 데서 멈추지 않고, 왜 이 순서가 자연스러운지까지 같이 보여 주려고 한다. 구현형 프로젝트는 진입점과 테스트를 먼저 보고, 분석형 프로젝트는 trace 질문과 filter target을 먼저 잡는 방식으로 읽으면 흐름이 편하다.

## 권장 읽기 순서

1. [HTTP Packet Analysis](http/README.md) - HTTP trace에서 질문 하나마다 어떤 frame과 header를 근거로 답해야 하는가?
2. [DNS Packet Analysis](dns/README.md) - DNS trace에서 query, response, authoritative 여부를 어떤 필드로 구분했는가?
3. [TCP and UDP Packet Analysis](tcp-udp/README.md) - TCP와 UDP의 차이를 실제 세그먼트와 datagram 증거로 어떻게 읽었는가?
4. [IP and ICMP Packet Analysis](ip-icmp/README.md) - IP header, fragmentation, ICMP 메시지를 trace 안에서 어디까지 설명할 수 있는가?
5. [Ethernet and ARP Packet Analysis](ethernet-arp/README.md) - Ethernet frame과 ARP 교환을 링크 계층 주소 관점에서 어떻게 읽었는가?
6. [802.11 Wireless Packet Analysis](wireless-802.11/README.md) - 무선 링크 계층에서는 beacon, probe, association이 어떤 순서로 보이는가?
7. [TLS Packet Analysis](tls-ssl/README.md) - 암호화 이후에도 TLS handshake에서 무엇은 보이고 무엇은 숨는가?
8. [HTTP/2 and QUIC Analysis](http2-quic/README.md) - HTTP/2 frame interleaving과 QUIC packet trace를 비교해 multiplexing, connection ID, transport-level HOL 차이를 어디서 읽는가?

## 공통으로 보는 근거

- 프로젝트 README와 `problem/README.md`
- `problem/Makefile`의 실행/검증 target
- 구현형은 `python/` 또는 `cpp/`, 분석형은 `analysis/src/`
- 테스트 파일과 `docs/concepts/`

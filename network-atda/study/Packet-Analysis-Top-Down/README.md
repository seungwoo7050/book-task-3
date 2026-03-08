# Packet Analysis Top-Down

HTTP에서 TLS까지 내려가며 패킷 캡처를 문제-증거-해설 구조로 정리한 트랙이다.

## 왜 이 트랙인가

공개 답안을 유지하되 answer-book이 아니라 학습 가이드를 목표로 재구성한다.

## 프로젝트 순서

1. [HTTP Packet Analysis](http/README.md) - `verified`
   핵심: 기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩이다.
2. [DNS Packet Analysis](dns/README.md) - `verified`
   핵심: DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩이다.
3. [TCP and UDP Packet Analysis](tcp-udp/README.md) - `verified`
   핵심: TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩이다.
4. [IP and ICMP Packet Analysis](ip-icmp/README.md) - `verified`
   핵심: IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩이다.
5. [Ethernet and ARP Packet Analysis](ethernet-arp/README.md) - `verified`
   핵심: 링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩이다.
6. [802.11 Wireless Packet Analysis](wireless-802.11/README.md) - `verified`
   핵심: 비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩이다.
7. [TLS Packet Analysis](tls-ssl/README.md) - `verified`
   핵심: TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩이다.

## 공통 규칙

- 코드 과제는 `problem/`과 `python/`을 분리한다.
- 패킷 분석 랩은 `problem/`과 `analysis/`를 분리한다.
- 시행착오와 회고는 `notion/`으로 밀어내고, 공개 README는 인덱스 역할만 맡긴다.

## 트랙 검증

- 전체 trace 점검: `make -C study/Packet-Analysis-Top-Down check-traces`
- 전체 답안 검증: `make -C study/Packet-Analysis-Top-Down test`

# 03. Packet Analysis Top-Down blog

이 트랙의 blog 시리즈는 고정 trace와 `tshark` 기반 검증 명령을 따라가며 답안을 어떻게 좁혀 가는지 복원한다. 구현 코드 대신 `problem/Makefile`, `analysis/src/*.md`, `docs/concepts/*wireshark*.md`, packet/frame evidence가 핵심 source set이다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| :--- | :--- | :--- |
| HTTP Packet Analysis | [`README.md`](http/README.md) | [`../../03-Packet-Analysis-Top-Down/http/README.md`](../../03-Packet-Analysis-Top-Down/http/README.md) |
| DNS Packet Analysis | [`README.md`](dns/README.md) | [`../../03-Packet-Analysis-Top-Down/dns/README.md`](../../03-Packet-Analysis-Top-Down/dns/README.md) |
| TCP and UDP Packet Analysis | [`README.md`](tcp-udp/README.md) | [`../../03-Packet-Analysis-Top-Down/tcp-udp/README.md`](../../03-Packet-Analysis-Top-Down/tcp-udp/README.md) |
| IP and ICMP Packet Analysis | [`README.md`](ip-icmp/README.md) | [`../../03-Packet-Analysis-Top-Down/ip-icmp/README.md`](../../03-Packet-Analysis-Top-Down/ip-icmp/README.md) |
| Ethernet and ARP Packet Analysis | [`README.md`](ethernet-arp/README.md) | [`../../03-Packet-Analysis-Top-Down/ethernet-arp/README.md`](../../03-Packet-Analysis-Top-Down/ethernet-arp/README.md) |
| TLS Packet Analysis | [`README.md`](tls-ssl/README.md) | [`../../03-Packet-Analysis-Top-Down/tls-ssl/README.md`](../../03-Packet-Analysis-Top-Down/tls-ssl/README.md) |
| 802.11 Wireless Packet Analysis | [`README.md`](wireless-802.11/README.md) | [`../../03-Packet-Analysis-Top-Down/wireless-802.11/README.md`](../../03-Packet-Analysis-Top-Down/wireless-802.11/README.md) |

## 읽는 순서
1. [`HTTP Packet Analysis`](http/README.md)와 [`DNS Packet Analysis`](dns/README.md)로 응용 계층 텍스트/이름 해석 프로토콜부터 본다.
2. [`TCP and UDP Packet Analysis`](tcp-udp/README.md), [`IP and ICMP Packet Analysis`](ip-icmp/README.md)로 전송/네트워크 계층을 이어 본다.
3. [`Ethernet and ARP Packet Analysis`](ethernet-arp/README.md), [`802.11 Wireless Packet Analysis`](wireless-802.11/README.md)로 링크 계층 차이를 정리한다.
4. [`TLS Packet Analysis`](tls-ssl/README.md)로 암호화 이후 관찰 가능한 정보와 한계를 묶는다.

## source-first 메모
- 분석형이므로 inline 증거는 `tshark` filter, frame number, answer snippet을 본문 중간에 직접 넣는다.
- CLI는 `make filter-*`, `make summary`, `make test` 순서를 기본으로 삼고, GUI `wireshark` 열기 명령은 선택으로만 적는다.
- trace가 짧아 교재 질문 일부가 비어 있는 경우, blog에서도 `관찰 불가` 판단을 그대로 보존한다.
- trace를 읽는 순서는 일반적인 개발자라면 택할 필터 순서를 기준으로 추론한다.

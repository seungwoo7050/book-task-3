# network-atda study

`network-atda`는 네트워크 학습 결과물을 `문제 -> 답 -> 검증 -> 개념 문서` 계약으로 정리한 study-first 아카이브다. GitHub 첫 화면에서 무엇을 풀었고, 답이 어디 있고, 어떤 명령으로 재검증하는지 바로 찾을 수 있게 공개 표면을 고정한다.

## 이 레포가 푸는 문제군

- 응용 계층 프로토콜을 socket 위에서 직접 구현하는 문제
- 손실/손상 채널에서 신뢰 전송 상태를 코드로 설명하는 문제
- Wireshark trace를 근거로 프로토콜 동작을 해석하는 문제
- ICMP 진단 도구와 라우팅 알고리즘으로 네트워크 계층을 재설명하는 문제
- 앞선 학습을 하나의 설명 가능한 game server capstone으로 통합하는 문제

## 단계별 학습 순서

| 단계 | 핵심 질문 | 시작점 |
| :--- | :--- | :--- |
| [`01. Application Protocols and Sockets`](study/01-Application-Protocols-and-Sockets/README.md) | 소켓 위에서 애플리케이션 규칙을 직접 구현하면 어떤 계약이 드러나는가 | [`Web Server`](study/01-Application-Protocols-and-Sockets/web-server/README.md) |
| [`02. Reliable Transport`](study/02-Reliable-Transport/README.md) | ACK, checksum, timer, sliding window가 신뢰 전송을 어떻게 만드는가 | [`RDT Protocol`](study/02-Reliable-Transport/rdt-protocol/README.md) |
| [`03. Packet Analysis Top-Down`](study/03-Packet-Analysis-Top-Down/README.md) | 패킷 trace만으로 무엇을 근거 있게 설명할 수 있는가 | [`HTTP Packet Analysis`](study/03-Packet-Analysis-Top-Down/http/README.md) |
| [`04. Network Diagnostics and Routing`](study/04-Network-Diagnostics-and-Routing/README.md) | ICMP, TTL, Bellman-Ford가 진단 도구와 라우팅 알고리즘으로 어떻게 이어지는가 | [`ICMP Pinger`](study/04-Network-Diagnostics-and-Routing/icmp-pinger/README.md) |
| [`05. Game Server Capstone`](study/05-Game-Server-Capstone/README.md) | 앞선 학습을 하나의 설명 가능한 서버 프로젝트로 어떻게 통합할 것인가 | [`Tactical Arena Server`](study/05-Game-Server-Capstone/tactical-arena-server/README.md) |

서버 개발자 관점에서 1회독 범위를 더 줄이고 싶다면 [`problem-subject-essential/README.md`](problem-subject-essential/README.md)를 먼저 읽는 편이 빠릅니다.
필수에 포함되지 않은 나머지 문제지는 [`problem-subject-elective/README.md`](problem-subject-elective/README.md)에 따로 모아 두었습니다.
종합 과제는 [`problem-subject-capstone/README.md`](problem-subject-capstone/README.md)에 따로 모아 둡니다.

## 프로젝트 카탈로그

| 단계 | 프로젝트 | 문제 | 이 레포의 답 | 검증 | 상태 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01-Application-Protocols-and-Sockets` | [`Web Server`](study/01-Application-Protocols-and-Sockets/web-server/README.md) | `Computer Networking: A Top-Down Approach`의 웹 서버 구현 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test` | `verified` |
| `01-Application-Protocols-and-Sockets` | [`UDP Pinger`](study/01-Application-Protocols-and-Sockets/udp-pinger/README.md) | `Computer Networking: A Top-Down Approach`의 UDP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` | `verified` |
| `01-Application-Protocols-and-Sockets` | [`SMTP Client`](study/01-Application-Protocols-and-Sockets/smtp-client/README.md) | `Computer Networking: A Top-Down Approach`의 SMTP 메일 클라이언트 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test` | `verified` |
| `01-Application-Protocols-and-Sockets` | [`Web Proxy`](study/01-Application-Protocols-and-Sockets/web-proxy/README.md) | `Computer Networking: A Top-Down Approach`의 HTTP 프록시 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test` | `verified` |
| `02-Reliable-Transport` | [`RDT Protocol`](study/02-Reliable-Transport/rdt-protocol/README.md) | `Computer Networking: A Top-Down Approach`의 rdt3.0/GBN 흐름을 현재 저장소 구조에 맞게 정리한 구현 프로젝트 | `python/src/` | `make -C study/02-Reliable-Transport/rdt-protocol/problem test` | `verified` |
| `02-Reliable-Transport` | [`Selective Repeat`](study/02-Reliable-Transport/selective-repeat/README.md) | 이 저장소에서 `Go-Back-N` 다음 단계 학습을 위해 직접 보강한 Selective Repeat 프로젝트 | `python/src/` | `make -C study/02-Reliable-Transport/selective-repeat/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`HTTP Packet Analysis`](study/03-Packet-Analysis-Top-Down/http/README.md) | `Computer Networking: A Top-Down Approach`의 HTTP Wireshark 랩을 현재 저장소의 `problem/analysis/docs` 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/http/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`DNS Packet Analysis`](study/03-Packet-Analysis-Top-Down/dns/README.md) | `Computer Networking: A Top-Down Approach`의 DNS Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/dns/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`TCP and UDP Packet Analysis`](study/03-Packet-Analysis-Top-Down/tcp-udp/README.md) | `Computer Networking: A Top-Down Approach`의 TCP/UDP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`IP and ICMP Packet Analysis`](study/03-Packet-Analysis-Top-Down/ip-icmp/README.md) | `Computer Networking: A Top-Down Approach`의 IP/ICMP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`Ethernet and ARP Packet Analysis`](study/03-Packet-Analysis-Top-Down/ethernet-arp/README.md) | `Computer Networking: A Top-Down Approach`의 Ethernet/ARP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`802.11 Wireless Packet Analysis`](study/03-Packet-Analysis-Top-Down/wireless-802.11/README.md) | `Computer Networking: A Top-Down Approach`의 802.11 Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`TLS Packet Analysis`](study/03-Packet-Analysis-Top-Down/tls-ssl/README.md) | `Computer Networking: A Top-Down Approach`의 TLS/SSL Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test` | `verified` |
| `03-Packet-Analysis-Top-Down` | [`HTTP/2 and QUIC Analysis`](study/03-Packet-Analysis-Top-Down/http2-quic/README.md) | HTTP/2 frame sequence와 QUIC packet trace를 비교해 multiplexing, stream, connection ID를 읽는 이 저장소의 직접 보강 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/http2-quic/problem test` | `verified` |
| `04-Network-Diagnostics-and-Routing` | [`ICMP Pinger`](study/04-Network-Diagnostics-and-Routing/icmp-pinger/README.md) | `Computer Networking: A Top-Down Approach`의 ICMP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` | `verified` |
| `04-Network-Diagnostics-and-Routing` | [`Traceroute`](study/04-Network-Diagnostics-and-Routing/traceroute/README.md) | ICMP/TTL 학습을 실제 경로 추적 도구로 연결하기 위해 이 저장소에서 직접 보강한 bridge 프로젝트 | `python/src/` | `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test` | `verified` |
| `04-Network-Diagnostics-and-Routing` | [`Distance-Vector Routing`](study/04-Network-Diagnostics-and-Routing/routing/README.md) | `Computer Networking: A Top-Down Approach`의 distance-vector 라우팅 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 | `python/src/` | `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test` | `verified` |
| `05-Game-Server-Capstone` | [`Tactical Arena Server`](study/05-Game-Server-Capstone/tactical-arena-server/README.md) | 이 저장소에서 누적한 네트워크 학습을 하나의 설명 가능한 서버로 묶기 위해 직접 설계한 신규 capstone 프로젝트 | `cpp/src/` | `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test` | `verified` |

## 검증 빠른 시작

- `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`
- `make -C study/02-Reliable-Transport/rdt-protocol/problem test`
- `make -C study/03-Packet-Analysis-Top-Down test`
- `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`
- `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test`

## 문서 지도

- [`study/README.md`](study/README.md) - 단계 인덱스와 읽는 순서
- [`study/blog/README.md`](study/blog/README.md) - 실제 소스와 검증 자산을 바탕으로 다시 쓴 프로젝트별 blog 인덱스
- [`docs/readme-contract.md`](docs/readme-contract.md) - 루트, 단계, 프로젝트, 하위 README의 공개 표면 계약
- [`docs/curriculum-map.md`](docs/curriculum-map.md) - 왜 이 순서로 단계를 구성했는지
- [`docs/project-set-audit.md`](docs/project-set-audit.md) - 현재 프로젝트 묶음의 강점과 의도적인 공백
- [`docs/repository-inventory.md`](docs/repository-inventory.md) - 현재 디렉터리 구조와 역할
- [`docs/project-template.md`](docs/project-template.md) - 새 프로젝트를 추가할 때 따를 기본 구조와 README 규칙
- [`docs/verification-matrix.md`](docs/verification-matrix.md) - canonical 검증 명령과 상태 표

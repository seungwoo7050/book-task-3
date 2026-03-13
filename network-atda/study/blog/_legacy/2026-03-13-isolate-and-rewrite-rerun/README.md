# network-atda blog

`study/blog/`는 `network-atda`의 공개 학습 로그 레이어다. 이 디렉터리는 루트 README나 `docs/`를 대체하지 않고, 각 독립 프로젝트를 `source-first` 방식으로 다시 읽는 chronological blog 시리즈만 모은다.

## 이 레이어의 기준
- 적용 단위는 항상 `독립 프로젝트`다.
- 기본 원천은 `README.md`, `problem/README.md`, `problem/Makefile`, 구현/분석 산출물, `tests`, `docs/`, `git log -- <project>`다.
- 소스만으로 chronology가 완전히 드러나지 않는 구간은 `일반적인 수준의 개발자`가 밟았을 합리적인 탐색 순서를 기준으로 추론해 적는다.
- 정확한 날짜 근거가 부족한 프로젝트는 `Day N / Session N`으로 기록한다.
- 구현형은 짧은 코드 조각을, 분석형은 `tshark` filter나 frame evidence를 inline 증거로 남긴다.
- `03-Packet-Analysis-Top-Down/tools`는 보조 도구 디렉터리이므로 blog 대상에서 제외한다.

## 트랙 인덱스

| 트랙 | 프로젝트 수 | 시작점 |
| :--- | :--- | :--- |
| [`01-Application-Protocols-and-Sockets`](01-Application-Protocols-and-Sockets/README.md) | `4` | [`Web Server`](01-Application-Protocols-and-Sockets/web-server/README.md) |
| [`02-Reliable-Transport`](02-Reliable-Transport/README.md) | `2` | [`RDT Protocol`](02-Reliable-Transport/rdt-protocol/README.md) |
| [`03-Packet-Analysis-Top-Down`](03-Packet-Analysis-Top-Down/README.md) | `7` | [`HTTP Packet Analysis`](03-Packet-Analysis-Top-Down/http/README.md) |
| [`04-Network-Diagnostics-and-Routing`](04-Network-Diagnostics-and-Routing/README.md) | `3` | [`ICMP Pinger`](04-Network-Diagnostics-and-Routing/icmp-pinger/README.md) |
| [`05-Game-Server-Capstone`](05-Game-Server-Capstone/README.md) | `1` | [`Tactical Arena Server`](05-Game-Server-Capstone/tactical-arena-server/README.md) |

## 프로젝트 카탈로그

### 01. Application Protocols and Sockets
- [`Web Server`](01-Application-Protocols-and-Sockets/web-server/README.md)
- [`UDP Pinger`](01-Application-Protocols-and-Sockets/udp-pinger/README.md)
- [`SMTP Client`](01-Application-Protocols-and-Sockets/smtp-client/README.md)
- [`Web Proxy`](01-Application-Protocols-and-Sockets/web-proxy/README.md)

### 02. Reliable Transport
- [`RDT Protocol`](02-Reliable-Transport/rdt-protocol/README.md)
- [`Selective Repeat`](02-Reliable-Transport/selective-repeat/README.md)

### 03. Packet Analysis Top-Down
- [`HTTP Packet Analysis`](03-Packet-Analysis-Top-Down/http/README.md)
- [`DNS Packet Analysis`](03-Packet-Analysis-Top-Down/dns/README.md)
- [`TCP and UDP Packet Analysis`](03-Packet-Analysis-Top-Down/tcp-udp/README.md)
- [`IP and ICMP Packet Analysis`](03-Packet-Analysis-Top-Down/ip-icmp/README.md)
- [`Ethernet and ARP Packet Analysis`](03-Packet-Analysis-Top-Down/ethernet-arp/README.md)
- [`TLS Packet Analysis`](03-Packet-Analysis-Top-Down/tls-ssl/README.md)
- [`802.11 Wireless Packet Analysis`](03-Packet-Analysis-Top-Down/wireless-802.11/README.md)

### 04. Network Diagnostics and Routing
- [`ICMP Pinger`](04-Network-Diagnostics-and-Routing/icmp-pinger/README.md)
- [`Traceroute`](04-Network-Diagnostics-and-Routing/traceroute/README.md)
- [`Distance-Vector Routing`](04-Network-Diagnostics-and-Routing/routing/README.md)

### 05. Game Server Capstone
- [`Tactical Arena Server`](05-Game-Server-Capstone/tactical-arena-server/README.md)

## 읽는 순서
1. 루트 [`../README.md`](../README.md)와 [`../README.md`](../README.md)의 프로젝트 카탈로그에서 전체 맥락을 먼저 확인한다.
2. 여기서 원하는 프로젝트의 blog `README.md`를 열어 어떤 source set으로 chronology를 복원했는지 확인한다.
3. `00-series-map.md`로 문제 경계, 제공물, 사용자 작성 답안, canonical verification을 고정한다.
4. `10-development-timeline.md` 이후의 numbered timeline 파일에서 실제 개발 흐름을 따라간다.
5. 구현 상세가 더 필요할 때만 원 프로젝트의 `docs/`와 실제 소스 파일로 내려간다.

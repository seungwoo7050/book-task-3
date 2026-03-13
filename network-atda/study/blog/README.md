# network-atda blog

`study/blog/`는 `network-atda`의 각 프로젝트를 다시 읽기 위한 안내 레이어다. 루트 README가 저장소 전체의 목차라면, 여기서는 한 프로젝트를 처음부터 어디까지 따라가면 되는지에 집중한다.

이번 리라이트는 기존 blog 초안이나 notion 메모를 입력으로 쓰지 않았다. 프로젝트 README, 문제 문서, 구현/분석 파일, 테스트, `problem/Makefile`, 실제 검증 출력만으로 다시 정리했다.

## 이 레이어를 읽는 법

1. 먼저 저장소 루트 README에서 전체 트랙 순서를 확인한다.
2. 원하는 트랙 README에서 왜 그 프로젝트를 그 순서로 읽는지 잡는다.
3. 프로젝트 폴더에 들어가면 `00-series-map.md`로 질문과 근거를 고정한다.
4. `01-evidence-ledger.md`로 세 단계 흐름을 보고, `10-development-timeline.md`에서 실제 서사를 읽는다.

## 트랙 지도

- [01. Application Protocols and Sockets](01-Application-Protocols-and-Sockets/README.md): TCP/UDP socket 위에서 HTTP, SMTP, ping, proxy를 직접 구현하며 응용 계층의 책임을 코드로 익히는 단계입니다.
- [02. Reliable Transport](02-Reliable-Transport/README.md): 손실과 손상이 있는 채널에서 송신자와 수신자가 어떤 상태를 기억해야 하는지 시뮬레이션으로 확인하는 단계입니다.
- [03. Packet Analysis Top-Down](03-Packet-Analysis-Top-Down/README.md): HTTP에서 HTTP/2와 QUIC 비교까지 내려가며 Wireshark trace를 문제-증거-해설 구조로 읽는 단계입니다.
- [04. Network Diagnostics and Routing](04-Network-Diagnostics-and-Routing/README.md): ICMP 기반 진단 도구와 distance-vector routing 구현으로 네트워크 계층 감각을 확장하는 단계입니다.
- [05. Game Server Capstone](05-Game-Server-Capstone/README.md): 소켓, 프로토콜, 상태 관리, persistence, 테스트 설계를 하나의 capstone으로 묶는 단계입니다.

## 프로젝트 목록

### 01. Application Protocols and Sockets
- [Web Server](01-Application-Protocols-and-Sockets/web-server/README.md): TCP 연결 하나를 받아 HTTP 요청, 파일 조회, 404 응답까지 어디서 나눠 구현했는가?
- [UDP Pinger](01-Application-Protocols-and-Sockets/udp-pinger/README.md): 연결 없는 UDP에서 손실과 timeout을 클라이언트 쪽 코드로 어떻게 드러냈는가?
- [SMTP Client](01-Application-Protocols-and-Sockets/smtp-client/README.md): SMTP 대화를 raw socket 위에서 단계별 명령으로 어떻게 끝까지 완주했는가?
- [Web Proxy](01-Application-Protocols-and-Sockets/web-proxy/README.md): 클라이언트 요청, origin fetch, cache 저장을 프록시 안에서 어떻게 이어 붙였는가?

### 02. Reliable Transport
- [RDT Protocol](02-Reliable-Transport/rdt-protocol/README.md): rdt3.0과 Go-Back-N의 핵심 차이를 같은 채널 모델 위에서 어떻게 드러냈는가?
- [Selective Repeat](02-Reliable-Transport/selective-repeat/README.md): 개별 ACK과 수신 버퍼링이 Go-Back-N 다음 단계에서 어떤 차이를 만드는가?

### 03. Packet Analysis Top-Down
- [HTTP Packet Analysis](03-Packet-Analysis-Top-Down/http/README.md): HTTP trace에서 질문 하나마다 어떤 frame과 header를 근거로 답해야 하는가?
- [DNS Packet Analysis](03-Packet-Analysis-Top-Down/dns/README.md): DNS trace에서 query, response, authoritative 여부를 어떤 필드로 구분했는가?
- [TCP and UDP Packet Analysis](03-Packet-Analysis-Top-Down/tcp-udp/README.md): TCP와 UDP의 차이를 실제 세그먼트와 datagram 증거로 어떻게 읽었는가?
- [IP and ICMP Packet Analysis](03-Packet-Analysis-Top-Down/ip-icmp/README.md): IP header, fragmentation, ICMP 메시지를 trace 안에서 어디까지 설명할 수 있는가?
- [Ethernet and ARP Packet Analysis](03-Packet-Analysis-Top-Down/ethernet-arp/README.md): Ethernet frame과 ARP 교환을 링크 계층 주소 관점에서 어떻게 읽었는가?
- [802.11 Wireless Packet Analysis](03-Packet-Analysis-Top-Down/wireless-802.11/README.md): 무선 링크 계층에서는 beacon, probe, association이 어떤 순서로 보이는가?
- [TLS Packet Analysis](03-Packet-Analysis-Top-Down/tls-ssl/README.md): 암호화 이후에도 TLS handshake에서 무엇은 보이고 무엇은 숨는가?
- [HTTP/2 and QUIC Analysis](03-Packet-Analysis-Top-Down/http2-quic/README.md): HTTP/2 frame interleaving과 QUIC packet trace를 비교해 multiplexing, connection ID, transport-level HOL 차이를 어디서 읽는가?

### 04. Network Diagnostics and Routing
- [ICMP Pinger](04-Network-Diagnostics-and-Routing/icmp-pinger/README.md): ICMP echo request/reply를 raw socket 위에서 어디까지 직접 조립하고 해석했는가?
- [Traceroute](04-Network-Diagnostics-and-Routing/traceroute/README.md): UDP probe와 ICMP 응답을 엮어 hop 단위 경로를 어떻게 복원했는가?
- [Distance-Vector Routing](04-Network-Diagnostics-and-Routing/routing/README.md): distance-vector가 topology 입력에서 최종 routing table로 수렴하는 과정을 어떻게 보여 줬는가?

### 05. Game Server Capstone
- [Tactical Arena Server](05-Game-Server-Capstone/tactical-arena-server/README.md): 제어 채널, authoritative simulation, persistence, 검증 하네스를 한 서버 안에서 어떻게 맞물리게 했는가?

## 이번 정리에서 제외한 경로

- `study/03-Packet-Analysis-Top-Down/tools`: 공용 보조 디렉터리라 blog 본문 대상에서 제외했다.

## 보관본

- 기존 초안은 `_legacy/` 아래에 그대로 남겨 두었다.

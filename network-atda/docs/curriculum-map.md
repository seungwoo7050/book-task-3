# Curriculum Map

현재 저장소는 top-level을 학습 단계 기준으로 정렬하고, 각 단계 안에서 프로젝트 README가 같은 공개 계약을 반복하도록 구성했습니다. 단순 챕터 순서를 복제하기보다, 한 프로젝트의 산출물이 다음 프로젝트의 선수 지식이 되도록 연결하는 데 초점을 둡니다.

## 1. Application Protocols and Sockets

1. `web-server`
2. `udp-pinger`
3. `smtp-client`
4. `web-proxy`

정적 웹 서버로 TCP 요청/응답의 최소 형태를 익힌 뒤, UDP timeout 처리, 텍스트 기반 메일 프로토콜, 프록시 캐시까지 점진적으로 복잡도를 올립니다.

## 2. Reliable Transport

1. `rdt-protocol`
2. `selective-repeat`

관찰만으로는 놓치기 쉬운 ACK, timer, sliding window의 상태를 코드로 직접 다룹니다. `selective-repeat`는 비교 학습을 위해 의도적으로 분리했습니다.

## 3. Packet Analysis Top-Down

1. `http`
2. `dns`
3. `tcp-udp`
4. `ip-icmp`
5. `ethernet-arp`
6. `wireless-802.11`
7. `tls-ssl`
8. `http2-quic`

HTTP에서 시작해 TLS까지 내려가며, 각 계층에서 어떤 field가 보이고 어떤 field는 보이지 않는지 trace 근거로 익힙니다. 마지막의 `http2-quic`는 최신 프로토콜이 기존 TCP/TLS 경계와 어떻게 달라지는지 비교하는 보강 슬롯입니다. 이 단계는 이후 구현 프로젝트를 다시 읽을 때 강한 복습 도구가 됩니다.

## 4. Network Diagnostics and Routing

1. `icmp-pinger`
2. `traceroute`
3. `routing`

ICMP Echo를 직접 만들고, TTL을 hop 추적으로 확장한 뒤, 마지막에는 분산 라우팅 테이블 계산으로 넘어갑니다. 패킷을 읽는 감각과 도구/알고리즘 구현 감각을 잇는 브리지 역할을 합니다.

## 5. Game Server Capstone

1. `tactical-arena-server`

앞선 단계에서 다룬 소켓, 프로토콜, 상태 관리, persistence, 테스트 설계를 하나의 설명 가능한 서버로 통합합니다. 학습용 레포를 공개 포트폴리오로 연결하는 마지막 단계입니다.

## 시작점 추천

- 소켓 프로그래밍이 처음이면 `study/01-Application-Protocols-and-Sockets/README.md`부터 시작합니다.
- 구현은 약하고 이론만 익숙하다면 `study/02-Reliable-Transport/README.md`와 `study/04-Network-Diagnostics-and-Routing/README.md`가 좋습니다.
- Wireshark로 네트워크를 보는 눈을 먼저 만들고 싶다면 `study/03-Packet-Analysis-Top-Down/README.md`부터 읽어도 됩니다.
- 이미 기초 프로젝트 경험이 있다면 `study/05-Game-Server-Capstone/README.md`를 먼저 보고 필요한 선행 프로젝트를 역추적할 수 있습니다.

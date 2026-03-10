# Curriculum Map

현재 저장소는 "구현 -> 관찰 -> 진단/알고리즘 -> 통합 프로젝트" 흐름으로 읽히도록 구성했습니다. 단순히 챕터 순서를 복제하는 대신, 서로 다른 프로젝트가 다음 프로젝트의 선수 지식이 되도록 연결하는 데 초점을 두었습니다.

## 1. Application Protocols and Sockets

1. `web-server`
2. `udp-pinger`
3. `smtp-client`
4. `web-proxy`

웹 서버로 TCP 요청/응답의 최소 형태를 익힌 뒤, UDP timeout 처리, 텍스트 기반 메일 프로토콜, 프록시 캐시까지 차근차근 복잡도를 올립니다.

## 2. Reliable Transport

1. `rdt-protocol`
2. `selective-repeat`

관찰만으로는 놓치기 쉬운 ACK, timer, sliding window의 상태를 코드로 직접 다룹니다. `selective-repeat`는 비교 학습을 위해 의도적으로 별도 프로젝트로 분리했습니다.

## 3. Packet Analysis Top-Down

1. `http`
2. `dns`
3. `tcp-udp`
4. `ip-icmp`
5. `ethernet-arp`
6. `wireless-802.11`
7. `tls-ssl`

HTTP에서 시작해 TLS까지 내려가며, 각 계층에서 어떤 field가 보이고 어떤 field는 보이지 않는지 trace 근거로 익힙니다. 이 트랙은 이후 구현 트랙을 다시 읽을 때 강한 복습 도구가 됩니다.

## 4. Network Diagnostics and Routing

1. `icmp-pinger`
2. `traceroute`
3. `routing`

ICMP Echo를 직접 만들고, TTL을 hop 추적으로 확장한 뒤, 마지막에는 분산 라우팅 테이블 계산으로 넘어갑니다. 패킷을 읽는 감각과 도구/알고리즘 구현 감각을 잇는 브리지 역할을 합니다.

## 5. Game Server Capstone

1. `tactical-arena-server`

앞선 트랙에서 다룬 소켓, 프로토콜, 상태 관리, persistence, 테스트 설계를 하나의 설명 가능한 서버로 통합합니다. 학습용 레포를 공개 포트폴리오로 연결하는 단계입니다.

## 어떤 독자에게 어떤 시작점이 좋은가

- 소켓 프로그래밍이 처음이면 `Application-Protocols-and-Sockets`부터 시작하세요.
- 이론은 아는데 구현이 약하다면 `Reliable-Transport`와 `Network-Diagnostics-and-Routing`이 좋습니다.
- Wireshark를 통해 네트워크를 "보는 눈"을 먼저 만들고 싶다면 `Packet-Analysis-Top-Down`부터 읽어도 괜찮습니다.
- 이미 기초 프로젝트 경험이 있다면 `Game-Server-Capstone`을 먼저 보고 필요한 선행 프로젝트를 역추적해도 됩니다.

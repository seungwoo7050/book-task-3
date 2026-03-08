
# Curriculum Map

## 1. Application-Protocols-and-Sockets

1. `web-server`
2. `udp-pinger`
3. `smtp-client`
4. `web-proxy`

응용 계층 프로토콜을 소켓 프로그래밍 입문에서 중개자 역할까지 확장하는 순서입니다.

## 2. Reliable-Transport

1. `rdt-protocol`
2. `selective-repeat`

레거시 과제는 GBN까지로 끝나지만, 문서 자체가 SR을 다음 비교 대상으로 암시하고 있어 독립 프로젝트를 추가했습니다.

## 3. Network-Diagnostics-and-Routing

1. `icmp-pinger`
2. `traceroute`
3. `routing`

패킷 수준 진단 도구에서 hop 단위 경로 인식으로 넘어간 뒤, 분산 라우팅 알고리즘으로 확장하는 흐름입니다.

## 4. Packet-Analysis-Top-Down

1. `http`
2. `dns`
3. `tcp-udp`
4. `ip-icmp`
5. `ethernet-arp`
6. `wireless-802.11`
7. `tls-ssl`

교재의 top-down 순서를 유지하되, 공개 답안은 `analysis/src/`로 격리해 탐색성을 높였습니다.

## 5. Game-Server-Capstone

1. `tactical-arena-server`

기존 네트워크 과제들을 채용용 산출물 하나로 묶는 최종 프로젝트입니다. TCP/UDP 분리, authoritative simulation, reconnect, persistence, bot/load smoke를 한 저장소 안에서 설명 가능한 형태로 정리합니다.

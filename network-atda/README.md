# Networking Study Archive

이 저장소는 현재 `study/` 아래의 소스와 문서를 기준으로 정리된 네트워크 학습 아카이브입니다. 목표는 단순 정답 보관이 아니라, **학습자에게 친절한 구조**를 제공하고, 이 저장소를 읽는 학생이 자신의 공개용 포트폴리오 저장소까지 발전시킬 수 있게 돕는 것입니다.

## 이 저장소가 돕는 것

- 어떤 문제를 왜 이 순서로 공부하는지 빠르게 파악할 수 있습니다.
- 각 프로젝트에서 무엇이 제공 자료이고 무엇이 공개 구현/공개 답안인지 분명히 구분합니다.
- `make test` 중심의 검증 명령을 따라가며 현재 동작하는 결과를 재현할 수 있습니다.
- 각 README는 학습 포인트와 현재 한계를 함께 드러내 포트폴리오 확장 방향까지 안내합니다.

## 추천 학습 순서

1. [`study/Application-Protocols-and-Sockets/README.md`](study/Application-Protocols-and-Sockets/README.md) - 소켓 프로그래밍과 응용 계층 프로토콜의 기본기를 잡습니다.
2. [`study/Reliable-Transport/README.md`](study/Reliable-Transport/README.md) - 손실/손상 환경에서 신뢰 전송이 어떻게 만들어지는지 구현으로 확인합니다.
3. [`study/Packet-Analysis-Top-Down/README.md`](study/Packet-Analysis-Top-Down/README.md) - HTTP에서 TLS까지 내려가며 패킷 trace를 근거로 읽는 연습을 합니다.
4. [`study/Network-Diagnostics-and-Routing/README.md`](study/Network-Diagnostics-and-Routing/README.md) - ICMP 진단 도구와 라우팅 알고리즘으로 네트워크 계층 감각을 넓힙니다.
5. [`study/Game-Server-Capstone/README.md`](study/Game-Server-Capstone/README.md) - 앞선 학습을 하나의 설명 가능한 서버 프로젝트로 묶습니다.

## 필수와 심화

처음부터 모든 프로젝트를 다 읽을 필요는 없습니다. 이 저장소에서는 **다음 학습의 선수 지식이 되는 축**을 `필수`, 범위를 넓히거나 비교 학습을 강화하는 프로젝트를 `심화`, 앞선 내용을 하나로 묶는 프로젝트를 `capstone`으로 봅니다.

### 필수 완주 경로

1. [`Web Server`](study/Application-Protocols-and-Sockets/web-server/README.md)
2. [`UDP Pinger`](study/Application-Protocols-and-Sockets/udp-pinger/README.md)
3. [`RDT Protocol`](study/Reliable-Transport/rdt-protocol/README.md)
4. [`HTTP Packet Analysis`](study/Packet-Analysis-Top-Down/http/README.md)
5. [`DNS Packet Analysis`](study/Packet-Analysis-Top-Down/dns/README.md)
6. [`TCP and UDP Packet Analysis`](study/Packet-Analysis-Top-Down/tcp-udp/README.md)
7. [`IP and ICMP Packet Analysis`](study/Packet-Analysis-Top-Down/ip-icmp/README.md)
8. [`ICMP Pinger`](study/Network-Diagnostics-and-Routing/icmp-pinger/README.md)
9. [`Traceroute`](study/Network-Diagnostics-and-Routing/traceroute/README.md)
10. [`Distance-Vector Routing`](study/Network-Diagnostics-and-Routing/routing/README.md)

응용 계층 구현 -> 신뢰 전송 -> 패킷 관찰 -> 진단/라우팅으로 이어지는 최소 학습 축입니다.

### 심화 확장

- [`SMTP Client`](study/Application-Protocols-and-Sockets/smtp-client/README.md)
- [`Web Proxy`](study/Application-Protocols-and-Sockets/web-proxy/README.md)
- [`Selective Repeat`](study/Reliable-Transport/selective-repeat/README.md)
- [`Ethernet and ARP Packet Analysis`](study/Packet-Analysis-Top-Down/ethernet-arp/README.md)
- [`802.11 Wireless Packet Analysis`](study/Packet-Analysis-Top-Down/wireless-802.11/README.md)
- [`TLS Packet Analysis`](study/Packet-Analysis-Top-Down/tls-ssl/README.md)

응용 프로토콜 범위 확장, 전송 계층 비교 심화, 링크/보안 계층 관찰 강화에 해당합니다.

### Capstone

- [`Tactical Arena Server`](study/Game-Server-Capstone/tactical-arena-server/README.md)

앞선 트랙에서 배운 내용을 하나의 설명 가능한 서버 프로젝트로 통합합니다.

## 빠른 시작

1. 루트 README를 읽고 관심 있는 트랙으로 이동합니다.
2. 각 프로젝트에서 `problem/README.md`를 먼저 읽습니다.
3. 구현 과제는 `python/README.md` 또는 `cpp/README.md`, 패킷 분석 과제는 `analysis/README.md`를 읽습니다.
4. 개념이 헷갈리면 `docs/README.md`와 `docs/concepts/`를 참고합니다.
5. 더 깊은 작업 기록이 필요할 때만 `notion/README.md`와 `notion-archive/`를 읽습니다.

## 검증 원칙

- `verified`는 현재 저장소 기준 대표 검증 명령을 통과한 상태를 뜻합니다.
- 구현 과제는 보통 `make -C <project>/problem test`를 canonical 검증으로 사용합니다.
- 패킷 분석 랩은 `problem/script/verify_answers.sh`를 감싼 `make test`를 canonical 검증으로 사용합니다.
- 외부 네트워크나 raw socket 권한에 따라 흔들리는 live 실행은 보조 재현 경로로만 취급하고, 완료 판정은 deterministic 검증을 우선합니다.

대표 검증 명령:

- `make -C study/Application-Protocols-and-Sockets/web-server/problem test`
- `make -C study/Reliable-Transport/rdt-protocol/problem test`
- `make -C study/Network-Diagnostics-and-Routing/routing/problem test`
- `make -C study/Packet-Analysis-Top-Down test`
- `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`

## 포트폴리오로 확장하기

- 테스트 통과만 적지 말고, **왜 이 범위까지만 구현했는지**와 **다음 확장 포인트**를 함께 적으세요.
- 구현 프로젝트는 요청/응답 로그, 실패 사례, 시연 명령을 남기고, 분석 프로젝트는 packet/frame 번호와 evidence를 남기면 훨씬 강해집니다.
- `notion/`은 과정을 공개 백업하는 용도입니다. README는 간결한 인덱스, `notion/`은 기술 노트라는 역할 분리를 유지하면 저장소가 훨씬 읽기 쉬워집니다.

## 문서 지도

- [`docs/README.md`](docs/README.md) - 저장소 전체 문서 인덱스
- [`docs/curriculum-map.md`](docs/curriculum-map.md) - 트랙과 프로젝트 순서 설계 이유
- [`docs/project-set-audit.md`](docs/project-set-audit.md) - 현재 프로젝트 묶음의 장단점과 의도적인 범위 설정
- [`docs/repository-inventory.md`](docs/repository-inventory.md) - 현재 저장소 구조와 디렉터리 역할
- [`docs/project-template.md`](docs/project-template.md) - 새 프로젝트를 추가할 때 따를 템플릿
- [`docs/verification-matrix.md`](docs/verification-matrix.md) - 현재 검증 명령과 상태 표

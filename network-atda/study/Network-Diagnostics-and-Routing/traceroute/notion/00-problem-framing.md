# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `Traceroute`
- 상태: `verified`
- 기준 검증: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test`
- 문제 배경: TTL을 하나씩 늘려 가며 경로를 드러내는 traceroute 원리를 직접 구현해 IP/ICMP 중첩 헤더를 읽는 프로젝트다.

## 이번 범위
- UDP probe를 보내고 raw ICMP 응답을 받아 hop별 경로를 출력한다.
- TTL, probe index, 목적지 포트를 조합해 응답과 원래 probe를 매칭한다.
- 도착지 `Port Unreachable`을 받으면 경로 추적을 종료한다.

## 제약과 전제
- UDP 송신 소켓과 raw ICMP 수신 소켓을 분리한다.
- Time Exceeded와 Destination Unreachable 파싱을 위해 중첩된 IP/ICMP/IP/UDP 헤더를 읽어야 한다.
- raw socket 권한이 필요하다.

## 성공 기준
- hop별 출력이 `*` timeout을 포함해 안정적으로 포맷된다.
- 목적지에 도착하면 ICMP type 3 code 3을 인식하고 종료한다.
- `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- IPv6 traceroute, Paris traceroute, AS/path enrichment는 다루지 않는다.
- DNS reverse lookup과 지리 정보 조회는 넣지 않았다.

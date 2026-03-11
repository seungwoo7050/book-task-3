# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `ICMP Pinger`
- 상태: `verified`
- 기준 검증: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 문제 배경: 운영체제의 `ping`을 그냥 사용하는 대신 ICMP Echo Request/Reply를 직접 만들어 raw socket과 checksum을 이해하는 프로젝트다.

## 이번 범위
- ICMP Echo Request 패킷을 직접 구성하고 Echo Reply를 파싱한다.
- RTT와 손실 통계를 출력한다.
- 단위 테스트와 실제 raw socket 실행을 분리해 관리한다.

## 제약과 전제
- raw socket은 관리자 권한 또는 `CAP_NET_RAW`가 필요하다.
- IPv4와 ICMP Echo에 집중하고, 본문/헤더 checksum은 직접 계산한다.
- 테스트는 순수 함수 검증과 실제 네트워크 검증을 분리한다.

## 성공 기준
- checksum, 패킷 빌드, 응답 파싱이 단위 테스트로 검증된다.
- 실행 시 성공 응답과 손실 통계를 읽을 수 있다.
- `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- IPv6 `ping6`, 고급 옵션, 플랫폼별 권한 차이 대응은 깊게 다루지 않는다.
- 운영체제 기본 `ping`과 동일한 모든 출력 형식을 재현하지 않는다.

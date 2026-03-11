# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `Selective Repeat`
- 상태: `verified`
- 기준 검증: `make -C study/02-Reliable-Transport/selective-repeat/problem test`
- 문제 배경: Go-Back-N 다음 단계로, 패킷별 타이머와 수신 버퍼를 갖는 Selective Repeat를 구현해 파이프라인 신뢰 전송의 비용 구조를 비교하는 프로젝트다.

## 이번 범위
- 제공 채널/패킷 모듈 위에서 Selective Repeat sender와 receiver를 구현한다.
- 손실과 손상 환경에서도 메시지를 순서대로 전달한다.
- 불필요한 전체 윈도 재전송 대신 필요한 패킷만 다시 보내는 구조를 만든다.

## 제약과 전제
- 시뮬레이터 인터페이스와 `test_messages.txt`는 기존 프로젝트와 호환되어야 한다.
- sender는 패킷별 ACK 상태와 개별 timeout을 관리해야 한다.
- receiver는 out-of-order 패킷을 버퍼링하되, 상위 전달은 순서를 지켜야 한다.

## 성공 기준
- 손실 없는 경우와 기본 fixture 테스트가 모두 통과한다.
- 재전송이 필요한 패킷만 다시 보내도록 sender 상태가 유지된다.
- `make -C study/02-Reliable-Transport/selective-repeat/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- SACK 옵션이나 실제 TCP 구현처럼 복잡한 최적화는 하지 않는다.
- 실제 네트워크 대신 시뮬레이터를 유지한다.

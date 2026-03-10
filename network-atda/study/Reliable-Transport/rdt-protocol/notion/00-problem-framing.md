# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `RDT Protocol`
- 상태: `verified`
- 기준 검증: `make -C study/Reliable-Transport/rdt-protocol/problem test`
- 문제 배경: 손실과 손상이 있는 채널 위에서 `rdt3.0`과 `Go-Back-N`을 직접 구현해 신뢰 전송의 핵심 개념을 익히는 프로젝트다.

## 이번 범위
- 제공된 `channel.py`, `packet.py` 위에서 `rdt3`와 `GBN` 송수신기를 구현한다.
- 손실/손상 환경에서도 `test_messages.txt`를 순서대로 전달해야 한다.
- stop-and-wait와 파이프라인 프로토콜의 차이를 코드 수준에서 비교한다.

## 제약과 전제
- 패킷 형식과 checksum 검사는 제공 모듈을 재사용한다.
- 구현은 단일 스레드 이벤트 루프를 유지해 상태 변화를 추적하기 쉽게 한다.
- GBN은 누적 ACK와 전체 윈도 재전송을 따른다.

## 성공 기준
- 패킷 모듈 테스트와 전송 시뮬레이션 테스트가 함께 통과한다.
- `rdt3`와 `GBN`이 둘 다 손실/손상 채널에서 메시지를 끝까지 전달한다.
- `make -C study/Reliable-Transport/rdt-protocol/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- Selective Repeat과 fast retransmit은 이 프로젝트 범위가 아니다.
- 실제 소켓 기반 전송이 아니라 시뮬레이터 채널 위에서 동작한다.

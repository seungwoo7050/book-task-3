# Selective Repeat 문제 사양

## 개요

`rdt-protocol`에서 사용한 것과 같은 unreliable channel model 위에 **Selective Repeat (SR)** 신뢰 전송 프로토콜을 구현한다. Go-Back-N과 달리 송신자는 timeout이 난 패킷만 다시 보내고, 수신자는 receive window 안에 들어온 out-of-order 패킷을 버퍼링한다.

## 핵심 개념

- **Sliding Window**: sender window와 receiver window를 동시에 유지한다.
- **Per-Packet Timers**: outstanding packet마다 개별 timeout을 추적한다.
- **Receiver Buffering**: 빠진 앞선 패킷이 도착할 때까지 순서 밖 패킷을 저장한다.
- **Selective ACK Behavior**: 유효한 패킷은 앞선 결손이 있어도 개별 ACK로 확인한다.

## 학습 목표

1. Selective Repeat가 왜 Go-Back-N보다 재전송 효율이 좋은지 코드로 비교한다.
2. 제공된 packet format과 unreliable channel helper를 바꾸지 않고 재사용한다.
3. 송신 측에서 패킷별 타이머와 ACK bookkeeping을 구현한다.
4. 수신 측에서 buffering과 in-order delivery를 구현한다.

## 과제 규칙

- 언어: Python 3 표준 라이브러리만 사용
- 제공 helper: `problem/code/channel.py`, `problem/code/packet.py`
- 기본 window size: `4`
- 테스트 데이터: `problem/data/test_messages.txt`
- 검증: `make test`는 root 권한 없이 로컬 SR 전송 검사를 수행한다.

# Selective Repeat 시리즈 맵

이 lab의 중심 질문은 "window를 유지한다는 공통점 아래에서, GBN과 달리 무엇을 packet마다 따로 기억해야 selective retransmission이 가능해지는가"다. 현재 구현은 sender 쪽에 `acked`와 `timers`, receiver 쪽에 `recv_buffer`를 두고 이 질문에 직접 답한다. 앞 packet이 비어 있어도 뒤 packet을 버리지 않고 ACK하며, timeout도 window 전체가 아니라 해당 packet에만 적용한다.

## 이 lab를 읽는 질문

- 왜 sender는 ACK 집합과 per-packet timer를 동시에 들고 있어야 하는가
- receiver buffer가 있으면 delivery와 ACK 시점은 어떻게 분리되는가
- duplicate old packet과 out-of-window future packet은 왜 다르게 처리되는가

## 이번에 사용한 근거

- `problem/README.md`
- `python/src/selective_repeat.py`
- `python/tests/test_selective_repeat.py`
- `problem/script/test_selective_repeat.sh`
- 2026-03-14 재실행 로그

## 이번 재실행에서 고정한 사실

- sender는 `send_base <= ack_seq < next_seq` 범위 안에서 ACK를 개별 packet 확인으로 처리한다.
- receiver는 `recv_base <= seq < recv_base + window_size`이면 out-of-order라도 `recv_buffer`에 저장하고 즉시 ACK를 보낸다.
- `recv_base`가 채워지면 `while recv_base in recv_buffer` 루프로 버퍼를 비우며 in-order delivery를 수행한다.
- 손실 채널 재실행에서 `seq=1`, `seq=3`, `seq=5`가 먼저 buffer되고, `seq=0` 또는 `seq=2`가 뒤늦게 도착한 뒤 한꺼번에 delivery가 이어졌다.

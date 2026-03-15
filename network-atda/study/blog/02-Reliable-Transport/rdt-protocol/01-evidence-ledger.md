# RDT Protocol Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/02-Reliable-Transport/rdt-protocol/problem/README.md`
- 구현 엔트리: `study/02-Reliable-Transport/rdt-protocol/python/src/rdt3.py`
- 구현 엔트리: `study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`
- 보조 테스트: `study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`
- 검증 스크립트: `study/02-Reliable-Transport/rdt-protocol/problem/script/test_rdt.sh`

## 핵심 코드 근거

- `rdt_send_receive()`: sender와 receiver 상태를 같은 loop 안에서 돌리며 alternating bit stop-and-wait를 구현한다.
- `current_pkt` + `timer_start`: stop-and-wait에서 현재 outstanding packet 하나만 추적한다.
- `gbn_send_receive()`: `base`, `next_seq`, `timer_start`로 sliding window와 oldest-unacked timer를 유지한다.
- `if payload == b"ACK" and ack_seq >= base`: GBN ACK를 cumulative으로 해석하는 지점이다.
- `expected_seq`만 수용하는 receiver branch: out-of-order packet을 buffer하지 않고 마지막 ACK만 재전송한다.

## 테스트 근거

`make -C network-atda/study/02-Reliable-Transport/rdt-protocol/problem test`

결과:

- `RDT 3.0 completes transfer` pass
- `GBN completes transfer` pass

보조 실행:

- `python3 python/src/rdt3.py --loss 0.2 --corrupt 0.1`
- `python3 python/src/gbn.py --loss 0.2 --corrupt 0.1 --window 4`

관찰:

- `rdt3.py`는 각 메시지마다 ACK를 받고 다음 payload로 넘어간다.
- `gbn.py`는 receiver가 `Out-of-order seq=4, re-sending ACK 2` 같은 로그를 내고, sender는 그 사이 window 전체를 다시 보낸다.

## 이번에 고정한 해석

- 이 lab의 핵심 비교축은 checksum 계산이 아니라 retransmission granularity다.
- GBN 구현은 송신 효율을 높이기 위해 여러 packet을 먼저 보낼 수 있지만, receiver buffer가 없어서 앞 packet 하나가 비면 뒤 packet도 결국 다시 보내게 된다.
- `python/tests/test_rdt.py`는 protocol loop 전체보다 packet helper 계약을 더 강하게 고정하므로, 실제 프로토콜 차이는 실행 로그를 함께 봐야 선명해진다.

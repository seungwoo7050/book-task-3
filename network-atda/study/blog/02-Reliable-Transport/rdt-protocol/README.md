# RDT Protocol Blog

이 문서 묶음은 `rdt-protocol`을 "신뢰 전송 이론"이 아니라 "같은 비신뢰 채널 위에서 stop-and-wait와 Go-Back-N이 무엇을 다르게 책임지는가"라는 질문으로 다시 읽는다. 현재 구현은 `rdt3.py`와 `gbn.py`를 분리해 두고, 하나는 alternating-bit와 단일 outstanding packet에, 다른 하나는 cumulative ACK와 sliding window에 무게를 둔다. 따라서 이 lab의 핵심은 개념 암기보다 retransmission 단위가 어떻게 바뀌는지 코드와 로그로 직접 비교하는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/02-Reliable-Transport/rdt-protocol/problem/README.md`
- 구현 경계: `README.md`, `python/README.md`, `python/src/rdt3.py`, `python/src/gbn.py`
- 테스트 근거: `python/tests/test_rdt.py`, `problem/script/test_rdt.sh`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/02-Reliable-Transport/rdt-protocol/problem test`
- 보조 실행 로그: `python3 python/src/rdt3.py --loss 0.2 --corrupt 0.1`, `python3 python/src/gbn.py --loss 0.2 --corrupt 0.1 --window 4`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/02-Reliable-Transport/rdt-protocol/problem test`
- 결과: `2 passed, 0 failed`
- 보조 실행: 두 구현 모두 손실/손상 채널에서 최종 `SUCCESS`까지 도달

## 지금 남기는 한계

- 실제 socket이나 RTT 측정이 아니라 시뮬레이션 채널 위 event loop다.
- `rdt3.py`는 alternating bit라 sequence space가 `0/1`에 고정된다.
- `gbn.py`는 out-of-order packet을 버리고 receiver buffer를 두지 않는다.

# Selective Repeat Blog

이 문서 묶음은 `selective-repeat`를 "GBN의 다음 이름"이 아니라 "재전송과 수신 버퍼링을 packet 단위로 분해하면 sender와 receiver 상태가 얼마나 달라지는가"라는 질문으로 다시 읽는다. 현재 구현은 `acked` 집합, `timers` 딕셔너리, `recv_buffer`를 따로 두고, timeout이 난 packet만 다시 보낸다. 따라서 이 lab의 핵심은 sliding window 자체보다 packet별 state를 끝까지 유지하는 비용을 드러내는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/02-Reliable-Transport/selective-repeat/problem/README.md`
- 구현 경계: `README.md`, `python/README.md`, `python/src/selective_repeat.py`
- 테스트 근거: `python/tests/test_selective_repeat.py`, `problem/script/test_selective_repeat.sh`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/02-Reliable-Transport/selective-repeat/problem test`
- 보조 실행 로그: `python3 python/src/selective_repeat.py --loss 0.2 --corrupt 0.1 --window 4`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/02-Reliable-Transport/selective-repeat/problem test`
- 결과: `2 passed, 0 failed`
- 보조 실행: 손실/손상 채널에서도 최종 `SUCCESS`와 `Retransmitting seq=` 로그를 확인

## 지금 남기는 한계

- sequence wraparound를 구현하지 않는다.
- 실제 병렬 timer thread 없이 단일 loop에서 `timers`를 순회한다.
- GBN 대비 성능 요약 표나 throughput 측정은 별도로 남기지 않는다.

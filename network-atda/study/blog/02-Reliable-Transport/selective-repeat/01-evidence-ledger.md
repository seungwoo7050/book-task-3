# Selective Repeat Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/02-Reliable-Transport/selective-repeat/problem/README.md`
- 구현 엔트리: `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`
- 보조 테스트: `study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`
- 검증 스크립트: `study/02-Reliable-Transport/selective-repeat/problem/script/test_selective_repeat.sh`

## 핵심 코드 근거

- `acked: set[int]` + `timers: dict[int, float]`: sender가 packet별 확인 여부와 timeout 시작 시점을 따로 보관한다.
- `recv_buffer: dict[int, str]`: receiver가 out-of-order payload를 버리지 않고 보관하는 핵심 상태다.
- `while send_base in acked`: base를 누적적으로 당기되, ACK 자체는 개별 packet 기준으로 쌓인다.
- `elif seq < recv_base`: 이미 전달이 끝난 오래된 duplicate packet은 buffer에 넣지 않고 re-ACK만 한다.
- `else: Ignored seq outside window`: receiver window 밖 미래 packet은 아예 무시한다.

## 테스트 근거

`make -C network-atda/study/02-Reliable-Transport/selective-repeat/problem test`

결과:

- `Selective Repeat completes transfer` pass
- `Sender retransmits selectively` pass

보조 실행:

- `python3 python/src/selective_repeat.py --loss 0.2 --corrupt 0.1 --window 4`

관찰:

- `seq=1`, `seq=3`, `seq=5`가 먼저 ACK되고도 곧바로 application delivery 되지는 않았다.
- `seq=0`, `seq=2`, `seq=4`가 늦게 도착하자 `Delivered seq=0`, `Delivered seq=1`처럼 buffer drain이 이어졌다.
- timeout 로그는 `Retransmitting seq=0`, `seq=2`, `seq=4`, `seq=6`처럼 packet 단위로 나타났다.

## 이번에 고정한 해석

- 이 lab의 핵심은 sender 효율보다 "ACK 시점과 delivery 시점을 분리할 수 있느냐"에 있다.
- Selective Repeat는 GBN보다 똑똑한 receiver를 택하는 대신 sender와 receiver 모두 더 많은 state를 관리해야 한다.
- 테스트 스크립트는 selective retransmission 로그 존재까지 확인하므로, 이 구현의 학습 포인트가 성능 숫자보다 retransmission granularity에 있음을 다시 드러낸다.

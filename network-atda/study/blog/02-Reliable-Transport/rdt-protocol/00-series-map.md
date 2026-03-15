# RDT Protocol 시리즈 맵

이 lab의 중심 질문은 "손실과 손상이 있는 같은 채널을 놓고, stop-and-wait와 Go-Back-N이 retransmission 단위를 어떻게 다르게 택하는가"다. 현재 저장소는 `rdt3.py`와 `gbn.py`를 나란히 두어 이 차이를 숨기지 않는다. `rdt3.py`는 한 번에 하나의 packet만 outstanding으로 두고 timeout 때 그 packet만 다시 보낸다. `gbn.py`는 `base`와 `next_seq`로 window를 운영하고, timeout이 나면 `base..next_seq-1` 범위를 통째로 다시 보낸다.

## 이 lab를 읽는 질문

- 단일 timer 하나만으로도 왜 stop-and-wait는 충분한가
- GBN에서 ACK가 개별 확인이 아니라 cumulative이라는 말이 코드에서는 어디에 나타나는가
- receiver가 buffer를 두지 않으면 sender 쪽 재전송 양상은 어떻게 달라지는가

## 이번에 사용한 근거

- `problem/README.md`
- `python/src/rdt3.py`
- `python/src/gbn.py`
- `python/tests/test_rdt.py`
- `problem/script/test_rdt.sh`
- 2026-03-14 재실행 로그

## 이번 재실행에서 고정한 사실

- `rdt3.py`는 `send_seq`를 `0/1`로 번갈아 쓰며 ACK 일치 여부를 `is_ack(ack_pkt, send_seq)`로 확인한다.
- `gbn.py`는 packet을 미리 전부 만들고 `base`, `next_seq`, `window_size`로 송신 window를 관리한다.
- GBN receiver는 기대한 `seq`만 전달하고, 나머지는 마지막 정상 ACK를 재전송한다.
- 손실 채널 재실행에서 `rdt3.py`는 `Timeout! Retransmitting seq=1`처럼 단일 재전송이 반복됐고, `gbn.py`는 `Retransmitting packets 2 to 5`처럼 범위 재전송이 나타났다.

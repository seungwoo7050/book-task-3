# RDT Protocol 개발 타임라인

현재 구현을 다시 읽으면 이 lab의 흐름은 "신뢰 전송을 한 번에 완성"한 이야기가 아니라, outstanding packet을 하나만 두는 모델에서 여러 개를 여는 모델로 사고를 넓혀 가는 순서에 가깝다. 코드 기준 전환점은 네 번이다.

## 1. 먼저 alternating bit stop-and-wait로 최소 신뢰 루프를 세운다

`rdt3.py`의 출발점은 단순하다. `send_seq`, `send_idx`, `current_pkt`, `awaiting_ack`만 있으면 한 번에 하나의 packet만 관리할 수 있다. sender는 packet 하나를 보내고 timer를 켠 뒤 ACK를 기다린다. receiver는 `expected_seq`와 맞는 packet만 수용하고, 중복이거나 손상된 packet에는 이전 ACK를 다시 보낸다.

2026-03-14 재실행에서도 이 구조가 그대로 보였다. 로그는 `Sent packet seq=1` 뒤 `Timeout! Retransmitting seq=1`이 반복됐고, ACK를 받기 전에는 다음 payload로 넘어가지 않았다. 즉 이 단계의 안정성은 throughput 희생과 맞바꾼 단순성 위에 서 있다.

## 2. packet helper 계약은 그대로 두고 sender state만 확장해 GBN으로 넘어간다

`gbn.py`는 packet 형식이나 channel helper를 바꾸지 않는다. 대신 sender state를 `base`와 `next_seq`로 확장한다. `while next_seq < min(base + window_size, total)` 루프가 이 전환점이다. 이제 sender는 ACK를 기다리기 전에 여러 packet을 연속으로 밀어 넣을 수 있다.

여기서 중요한 건 timer가 packet마다 하나씩 생기지 않는다는 점이다. GBN은 가장 오래된 outstanding packet 기준으로 timer 하나만 둔다. 그래서 ACK가 누적되면 timer를 끄거나 다시 시작하면 된다.

## 3. receiver는 더 똑똑해지지 않고, 그 제약이 GBN의 재전송 패턴을 만든다

GBN receiver는 `seq == expected_seq`만 수용한다. 나머지는 버리고 마지막 정상 ACK를 재전송한다. 이 때문에 sender가 앞 packet 하나를 잃으면, 뒤 packet이 실제로 도착했더라도 receiver는 전달하지 못한다.

이번 재실행에서 이 제약이 선명하게 드러났다. `seq=2`가 비어 있는 동안 receiver는 `seq=3`, `seq=4`, `seq=6`에 대해 계속 `re-sending ACK 1` 또는 `ACK 2`만 보냈고, sender는 결국 `Retransmitting packets 2 to 5`, `Retransmitting packets 3 to 6`처럼 window 전체를 다시 보냈다. 이 lab가 이후 Selective Repeat로 이어지는 이유가 바로 여기 있다.

## 4. 테스트는 성공 여부만 고정하고, 프로토콜 차이는 실행 로그가 채운다

정식 테스트 스크립트는 두 구현이 최종적으로 transfer를 완료하는지만 본다. `python/tests/test_rdt.py`도 packet helper correctness에 집중한다. 그래서 이 lab를 제대로 읽으려면 test pass만으로 끝내면 안 되고, 실제 실행 로그에서 `single retransmission`과 `range retransmission`의 차이를 함께 봐야 한다.

결국 이 lab의 산출물은 "손실 채널에서도 성공했다"보다 "성공에 이르는 방식이 왜 이렇게 다른가"를 비교할 수 있는 기준선이다.

## 지금 남는 한계

구현은 학습용으로는 충분하지만, 실제 transport stack이라고 부르기엔 범위가 작다. 시뮬레이션 채널, 단일 event loop, `rdt3.py`의 1-bit sequence space, GBN receiver의 no-buffer 정책이 모두 명시적이다. 그래서 이 lab는 완성품보다 다음 단계 비교 기준점으로 읽는 편이 정확하다.

# Structure Outline

## Chosen arc

1. business RPC가 아니라 transport minimum viable path라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 successful round trip과 split/error 경계를 먼저 보여 준다.
3. frame boundary recovery, pending correlation map, timeout/disconnect cleanup을 invariant로 정리한다.
4. 마지막에는 TLS, streaming, discovery가 아직 없다는 점을 분리한다.

## Why this structure

- 이 랩은 transport semantics가 전부라서 framing과 pending map을 초반부터 함께 보여 주는 편이 맞다.
- split chunk와 timeout은 작은 실험 출력이 강한 근거라서 early evidence로 적합하다.
- malformed JSON ignore 정책은 source-only nuance라 invariant 장에서 분명히 적는 편이 좋다.

## Rejected alternatives

- RPC 일반론을 길게 푸는 구조는 버렸다.
- handler 구현을 중심에 두는 구조도 버렸다.
- discovery나 retry 얘기를 미리 끌어오는 서사는 현재 범위를 벗어나 제외했다.

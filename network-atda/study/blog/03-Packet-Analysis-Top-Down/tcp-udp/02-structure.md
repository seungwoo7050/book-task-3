# TCP and UDP Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: TCP와 UDP를 같은 trace scale에서 어떻게 비교할지 먼저 고정한다.
- `10-development-timeline.md`: handshake -> data burst -> UDP minimal header 순으로 전송 계층 시야를 정리한다.
- `01-evidence-ledger.md`: `tshark` 필터와 answer markdown 계산 근거를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- TCP와 UDP를 "신뢰적 vs 비신뢰적" 한 줄 비교로 축소하지 않는다.
- TCP에서는 handshake, seq/ack, window, throughput 추정이 어떻게 이어지는지 보여 준다.
- UDP에서는 field 수가 적다는 사실이 design choice라는 점을 남긴다.

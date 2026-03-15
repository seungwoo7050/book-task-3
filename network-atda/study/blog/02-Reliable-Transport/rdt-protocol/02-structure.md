# RDT Protocol 구조 메모

## 문서 구성 의도

- `00-series-map.md`: stop-and-wait와 GBN을 어떤 비교 질문으로 읽을지 먼저 고정한다.
- `10-development-timeline.md`: single outstanding packet에서 sliding window로 넘어가는 전환을 chronology로 복원한다.
- `01-evidence-ledger.md`: source, test, rerun log를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- 이 lab를 "rdt3.0 구현" 하나로 축소하지 않고 `rdt3.py`와 `gbn.py`의 직접 비교로 읽는다.
- timer가 packet 하나에 붙는지, window의 oldest outstanding packet에 붙는지 차이를 중심에 둔다.
- receiver buffer 부재, simulated channel, alternating-bit 제한을 한계로 분리한다.

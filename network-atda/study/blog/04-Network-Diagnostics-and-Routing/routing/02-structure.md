# Distance-Vector Routing 구조 메모

## 문서 구성 의도

- `00-series-map.md`: Bellman-Ford가 distributed round simulation으로 바뀌는 지점을 먼저 고정한다.
- `10-development-timeline.md`: topology load -> node initialization -> DV exchange -> convergence output 순으로 구현 축을 정리한다.
- `01-evidence-ledger.md`: source, tests, rerun output을 짧게 묶는다.

## 이번 재작성에서 강조한 점

- shortest path 공식보다 node-local state update를 중심으로 설명한다.
- synchronous round model을 명시적으로 드러낸다.
- count-to-infinity mitigation 부재를 한계로 남긴다.

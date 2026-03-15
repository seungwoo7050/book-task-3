# Tactical Arena Server 구조 메모

## 문서 구성 의도

- `00-series-map.md`: control plane, realtime plane, simulation, persistence, verification을 어떤 질문으로 묶을지 먼저 고정한다.
- `10-development-timeline.md`: protocol layer에서 room-authoritative simulation과 verification harness까지 확장되는 흐름을 chronology로 정리한다.
- `01-evidence-ledger.md`: source, unit tests, integration/load/demo evidence를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- capstone을 "모든 걸 했다"가 아니라 "경계를 설명 가능한 상태로 묶었다"로 읽는다.
- protocol codec, `MatchState`, repository transaction, scenario harness를 각각 별도 축으로 설명한다.
- production non-goals를 끝까지 숨기지 않는다.

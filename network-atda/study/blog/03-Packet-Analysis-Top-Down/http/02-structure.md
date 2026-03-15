# HTTP Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: trace 네 개가 어떤 서로 다른 질문을 맡는지 먼저 정리한다.
- `10-development-timeline.md`: basic -> conditional -> long document -> embedded objects 순으로 해석 관점을 확장한다.
- `01-evidence-ledger.md`: `tshark` 필터와 answer markdown를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- HTTP 일반론보다 trace 시나리오별 관찰 포인트 차이를 중심에 둔다.
- `304`와 body omission, `Content-Length`와 segment count, embedded object fetch ordering을 각각 분리해 설명한다.
- `HTTP/2`와의 비교는 이 문서에 섞지 않고 다음 lab로 넘긴다.

# DNS Packet Analysis 구조 메모

## 문서 구성 의도

- `00-series-map.md`: 이 lab를 "짧은 trace가 허락하는 해석 범위"라는 질문으로 먼저 고정한다.
- `10-development-timeline.md`: nslookup trace에서 web trace로 넘어가며 보이는 것과 안 보이는 것을 chronology로 정리한다.
- `01-evidence-ledger.md`: answer markdown와 `tshark` 필터 출력을 짧게 묶는다.

## 이번 재작성에서 강조한 점

- trace limitation을 첫 문단에서 숨기지 않는다.
- malformed MX answer와 extraneous data 문제를 "답을 못 했다"가 아니라 "현재 증거가 끊기는 지점"으로 설명한다.
- DNS 일반론보다 실제 frame 번호와 필터 출력으로 돌아오는 습관을 중심에 둔다.

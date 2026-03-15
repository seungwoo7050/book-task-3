# Traceroute 구조 메모

## 문서 구성 의도

- `00-series-map.md`: probe/reply correlation rule을 먼저 고정한다.
- `10-development-timeline.md`: TTL ladder, port mapping, ICMP parse, termination rule 순으로 구현 축을 정리한다.
- `01-evidence-ledger.md`: source, unit tests, live timeout caveat를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- traceroute를 출력 유틸리티가 아니라 correlation algorithm으로 설명한다.
- embedded UDP port parse를 중심에 둔다.
- live rerun 미완료를 환경 경계로 분명히 남긴다.

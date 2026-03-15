# ICMP Pinger 구조 메모

## 문서 구성 의도

- `00-series-map.md`: raw ICMP implementation이 실제로 어디까지 manual work인지 먼저 고정한다.
- `10-development-timeline.md`: checksum -> packet build -> reply parse -> statistics 순으로 구현 축을 정리한다.
- `01-evidence-ledger.md`: source, deterministic tests, live timeout caveat를 짧게 묶는다.

## 이번 재작성에서 강조한 점

- packet bytes를 직접 만드는 부분을 중심에 둔다.
- fake socket test가 lab의 핵심 검증 surface라는 점을 분명히 적는다.
- live run 미완료를 숨기지 않고 현재 환경 경계로 남긴다.

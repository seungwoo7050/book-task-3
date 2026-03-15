# Web Server 구조 메모

- `00-series-map.md`: 서버 생애주기의 질문을 먼저 잡는다.
- `10-development-timeline.md`: accept -> parse -> file read -> response -> close 흐름을 복원한다.
- `01-evidence-ledger.md`: MIME map, 404 분기, thread-per-connection 근거를 남긴다.

이번 재작성에서는 "HTTP 구현 전체"보다 "가장 작은 정적 파일 서버"라는 현재 범위를 선명하게 두었다.

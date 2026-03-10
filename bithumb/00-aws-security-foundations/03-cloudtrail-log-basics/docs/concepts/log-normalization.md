# 로그 정규화

- 원본 로그 포맷이 달라도 `occurred_at`, `source`, `event_name`, `actor`, `resource_id` 같은 공통 필드를 정하면 이후 분석 코드가 단순해집니다.
- DuckDB + Parquet는 로컬에서도 security lake 감각을 익히기에 충분한 조합입니다.

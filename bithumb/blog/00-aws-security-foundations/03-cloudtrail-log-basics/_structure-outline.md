# 03 CloudTrail Log Basics structure outline

## 중심 질문

- 이 lab이 왜 "로그 fixture를 읽는다"가 아니라 "queryable local lake를 만든다"는 이야기로 읽혀야 하는지
- pytest의 깨끗한 tmp DB와 CLI의 누적 `.artifacts` 동작을 어떻게 같이 설명해야 하는지

## 글 흐름

1. CloudTrail과 VPC Flow Logs를 같은 `EventRecord`로 누르는 이유로 시작한다.
2. DuckDB와 Parquet를 동시에 남기는 장면을 저장 구조 전환점으로 둔다.
3. event summary / actor summary / time range 테스트로 queryability를 증명한다.
4. CLI append 동작과 누적 count를 마지막에 남겨 현재 한계를 분명히 한다.

## 반드시 남길 증거

- `normalize_cloudtrail_events()`, `normalize_vpc_flow_logs()`
- `ingest_records()`의 `CREATE TABLE IF NOT EXISTS` + `INSERT` + `COPY PARQUET`
- `test_etl.py`의 summary와 time range assertion
- `2026-03-14` CLI `ingested 4 records`
- `2026-03-14` pytest `1 passed in 0.05s`
- `2026-03-14` DuckDB 조회에서 event count가 모두 `3`으로 누적된 사실

## 반드시 피할 서술

- 원본 로그를 모두 보존한 것처럼 쓰는 설명
- DuckDB/Parquet를 단순 저장 포맷으로만 다루고 queryability를 빼먹는 문장
- CLI 산출물이 항상 깨끗한 재실행이라고 오해하게 만드는 표현
- detection query까지 이미 이 lab이 맡는 것처럼 보이게 하는 과장

## 톤 체크

- chronology는 `정규화 -> 적재 -> 질의 검증 -> 누적 동작 메모` 순서로 살아 있어야 한다.
- 홍보문보다 "무엇이 queryable해졌는가"와 "무엇이 아직 append형인가"가 함께 읽히는 탐색형 톤을 유지한다.

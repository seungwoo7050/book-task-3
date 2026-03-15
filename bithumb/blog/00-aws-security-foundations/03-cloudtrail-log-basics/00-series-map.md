# 03 CloudTrail Log Basics series map

이 시리즈는 `03-cloudtrail-log-basics`를 "로그 두 개를 읽는 ETL"이 아니라, 이후 security lake와 capstone이 공통으로 기대는 `EventRecord` 계약과 local lake 산출물을 만드는 프로젝트로 읽는다. 핵심은 CloudTrail과 VPC Flow Logs를 같은 필드 집합으로 정규화하고, DuckDB + Parquet로 남기고, 집계 질의가 실제로 돌아감을 테스트로 잠가 두는 데 있다. 다만 CLI는 `.artifacts/log-basics.duckdb`를 매번 append만 하므로 데모 산출물은 idempotent하지 않다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   raw log를 공통 이벤트 구조로 누르고, queryable storage에 적재하고, 테스트와 실제 재실행이 어디서 달라지는지 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 왜 원본 로그 보존보다 먼저 공통 필드 계약을 세워야 했는가
- DuckDB와 Parquet를 함께 남기는 일이 이후 lake 단계와 어떻게 이어지는가
- pytest는 안정적으로 통과하는데 CLI 재실행 산출물은 왜 누적되는가

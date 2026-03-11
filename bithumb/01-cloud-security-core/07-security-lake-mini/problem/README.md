# 문제 정리

## 원래 문제

Security Lake 개념을 로컬로 축소 구현해, 로그를 저장하고 미리 정의한 detection query로 이상 행위를 찾아야 합니다.
핵심은 적재와 탐지가 한 흐름이라는 점을 작은 규모에서 재현하는 것입니다.

## 제공된 자료

- `problem/data/cloudtrail_suspicious.json`
- local DuckDB 경로와 Parquet 경로
- preset detection query 묶음

## 제약

- 로컬 단일 테이블 흐름에 집중합니다.
- 분산 저장소나 대용량 최적화는 다루지 않습니다.

## 통과 기준

- fixture가 lake DB와 Parquet 파일로 적재되어야 합니다.
- detection query 결과가 `LAKE-001`부터 `LAKE-005`까지 순서대로 나와야 합니다.
- CLI가 JSON alert 목록을 반환해야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- VPC Flow Logs join
- 다중 테이블 correlation
- 분산 lakehouse 아키텍처

# 문제 정리

## 원래 문제

CloudTrail과 VPC Flow Logs를 그대로 저장하는 대신, 이후 query와 detection에 재사용할 수 있는 공통 이벤트 구조로 정리해야 합니다.
핵심은 로그를 “수집”이 아니라 “분석 가능한 입력”으로 바꾸는 것입니다.

## 제공된 자료

- `problem/data/cloudtrail_events.json`
- `problem/data/vpc_flow_logs.json`
- DuckDB와 Parquet 기반 로컬 적재 경로

## 제약

- 실제 운영 규모의 대용량 적재는 다루지 않습니다.
- 정규화 필드는 이후 프로젝트가 쓰는 최소 공통 필드로 제한합니다.

## 통과 기준

- fixture를 읽어 DuckDB table과 Parquet 파일을 생성해야 합니다.
- 이벤트 이름, actor, 기간 집계가 테스트로 보장되어야 합니다.
- 이후 lake 프로젝트가 재사용할 수 있는 구조여야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- 전체 CloudTrail 스키마 보존
- 분산 적재 파이프라인
- detection query 자체

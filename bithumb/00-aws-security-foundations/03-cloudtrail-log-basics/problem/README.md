# 문제 정리

## 문제 요약

CloudTrail과 VPC Flow Logs를 그대로 읽는 대신, 이후 query와 detection에 재사용할 수 있는 공통 이벤트 구조로 정리합니다.

## 입력

- CloudTrail fixture JSON
- VPC Flow Logs fixture JSON

## 출력

- 정규화된 이벤트
- DuckDB table
- Parquet 파일

## 학습 포인트

로그를 적재하는 이유가 저장 자체가 아니라 분석 가능성이라는 점을 체감하는 데 있습니다.

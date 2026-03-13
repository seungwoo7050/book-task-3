# 03 CloudTrail Log Basics 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- raw security log를 읽기 좋은 예시가 아니라, 후속 detection query가 바로 사용할 수 있는 `EventRecord`와 lake 산출물로 복원한다.
- 글은 `정규화 -> 적재 -> 질의 검증` 세 단계로 밀어 붙여 “queryable log”가 언제 생겼는지 보이게 한다.

## 먼저 붙들 소스 묶음
- [`../../../00-aws-security-foundations/03-cloudtrail-log-basics/README.md`](../../../00-aws-security-foundations/03-cloudtrail-log-basics/README.md)
- [`../../../00-aws-security-foundations/03-cloudtrail-log-basics/problem/README.md`](../../../00-aws-security-foundations/03-cloudtrail-log-basics/problem/README.md)
- [`../../../00-aws-security-foundations/03-cloudtrail-log-basics/docs/concepts/log-normalization.md`](../../../00-aws-security-foundations/03-cloudtrail-log-basics/docs/concepts/log-normalization.md)
- [`../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/README.md`](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/README.md)
- [`../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py`](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py)
- [`../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py`](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - EventRecord contract와 DuckDB/Parquet verify 경로를 먼저 제시한다.
- `10-development-timeline.md`
  - 도입: CloudTrail과 VPC Flow Logs를 왜 같은 분석 surface로 눌러야 했는지 설명한다.
  - Phase 1. 두 로그를 같은 `EventRecord`로 눌렀다.
  - Phase 2. DuckDB와 Parquet를 동시에 남겼다.
  - Phase 3. 집계 쿼리와 time range를 테스트로 잠갔다.
  - 마무리: 다음 프로젝트에서 lake 적재 결과가 어떻게 `LAKE-*` alert로 재사용되는지 질문을 남긴다.

## 강조할 코드와 CLI
- 코드 앵커: `normalize_cloudtrail`, `normalize_flow_logs`, DuckDB insert, Parquet export, aggregate query helpers
- CLI 앵커: `pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests`, README sample query command
- 개념 훅: log normalization의 핵심은 포맷을 예쁘게 바꾸는 것이 아니라 query contract를 통일하는 데 있다는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.

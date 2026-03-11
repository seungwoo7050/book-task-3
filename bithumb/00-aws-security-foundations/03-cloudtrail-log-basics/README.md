# 03 CloudTrail Log Basics

## 풀려는 문제

CloudTrail과 VPC Flow Logs를 그대로 저장하는 것만으로는 이후 detection query를 만들기 어렵습니다.
이 프로젝트는 원본 로그를 queryable한 공통 이벤트 구조로 정리하는 가장 작은 ETL 단계를 구현합니다.

## 내가 낸 답

- CloudTrail과 VPC Flow Logs fixture를 `occurred_at`, `source`, `event_name`, `actor` 중심 공통 구조로 정규화합니다.
- 로컬에서 바로 질의할 수 있도록 DuckDB table과 Parquet 산출물을 함께 생성합니다.
- 작은 fixture만으로도 적재와 집계가 반복 검증되도록 단순한 ETL 흐름을 유지합니다.
- 07번 security lake와 10번 캡스톤이 이어받을 로그 입력 형태를 먼저 고정합니다.

## 입력과 출력

- 입력: `problem/data/cloudtrail_events.json`, `problem/data/vpc_flow_logs.json`
- 출력: `event_records` 테이블, Parquet 파일, 집계 가능한 정규화 레코드

## 검증 방법

```bash
make venv
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## 현재 상태

- `verified`
- 로컬 fixture 기준 ETL 재현 가능
- 07번과 10번에서 다시 사용할 로그 입력 구조를 이미 제공합니다.

## 한계와 다음 단계

- 실제 CloudTrail 전체 스키마를 모두 보존하지는 않습니다.
- 분산 적재와 대용량 파이프라인 최적화는 다루지 않고, 07번에서 detection query 단계로 확장합니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)

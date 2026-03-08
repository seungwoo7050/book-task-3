# 03 CloudTrail Log Basics

## Status

`verified`

## Problem Scope

- CloudTrail/VPC Flow Logs 스타일 JSON 정규화
- DuckDB 적재
- principal/event_name/time range 기준 요약

## Build

```bash
cd python
PYTHONPATH=src python -m cloudtrail_log_basics.etl ../problem/data/cloudtrail_events.json ../problem/data/vpc_flow_logs.json
```

## Test

```bash
cd study2
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## Learned

CloudTrail을 단순 로그 파일이 아니라 “정규화된 이벤트 레코드”로 만들 수 있어야 Security Lake와
이상 행위 탐지가 이어진다.

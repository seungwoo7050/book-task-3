# 03 CloudTrail Log Basics - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `etl.py`, `test_etl.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- CloudTrail과 VPC Flow Logs를 그대로 두지 않고 이후 탐지에 재사용할 공통 이벤트 구조로 어떻게 정리할까
- DuckDB와 Parquet를 학습용 로그 적재 경로로 쓰면 어디까지 설명 가능할까

## 실제 구현 표면

- CloudTrail과 VPC Flow Logs를 공통 `EventRecord` 구조로 정규화합니다.
- DuckDB `event_records` 테이블과 Parquet 파일을 동시에 생성합니다.
- event name, actor, 시간 범위 집계를 작은 helper 함수로 바로 확인할 수 있습니다.

## 대표 검증 엔트리

- `PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json`
- `PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../00-aws-security-foundations/03-cloudtrail-log-basics/README.md)
2. [문제 정의](../../../00-aws-security-foundations/03-cloudtrail-log-basics/problem/README.md)
3. [실행 진입점](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/README.md)
4. [대표 테스트](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py)
5. [핵심 구현](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../00-aws-security-foundations/03-cloudtrail-log-basics/README.md)
- [problem/README.md](../../../00-aws-security-foundations/03-cloudtrail-log-basics/problem/README.md)
- [python/README.md](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/README.md)
- [etl.py](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py)
- [test_etl.py](../../../00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

# 디버그 로그

## 실제로 자주 막히는 지점

- `resource_id`를 어떤 필드에서 뽑을지 이벤트 종류마다 다를 수 있습니다. archive에서도 이 판단이 정규화의 핵심이라고 정리되어 있습니다.
- DuckDB 적재가 끝나도 Parquet 파일이 생성되지 않으면 이후 lake 단계와 연결이 끊깁니다.
- “정규화 성공”과 “질의 가능”은 다릅니다. 집계 쿼리까지 확인해야 합니다.

## 이미 확인된 테스트 시나리오

- `test_etl_ingests_cloudtrail_and_vpc_flow_logs`: 두 로그 소스가 함께 적재되는지 확인합니다.
- 같은 테스트 안에서 `summarize_by_event_name`, `summarize_by_actor`, `within_time_range` 결과를 모두 검증합니다.
- 기대 결과는 `CreateAccessKey`, `PutBucketAcl`, `flow:22`, `flow:443` 네 이벤트와 시간 범위 내 2건 집계입니다.

## 다시 검증할 명령

```bash
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_etl.py](../python/tests/test_etl.py)
- ETL 구현: [../python/src/cloudtrail_log_basics/etl.py](../python/src/cloudtrail_log_basics/etl.py)
- 이전 재현 기록: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

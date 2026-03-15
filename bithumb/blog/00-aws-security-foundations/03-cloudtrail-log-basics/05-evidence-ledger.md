# 03 CloudTrail Log Basics evidence ledger

- 복원 원칙: 기존 blog 본문은 제외하고 `README/problem/docs`, ETL 소스, pytest, 실제 CLI/DB 재실행 결과만 근거로 썼다.
- 날짜 고정: 아래 실행 결과는 `2026-03-14` 기준이다.
- 프로젝트 성격: 이 lab의 산출물은 원본 로그 보관이 아니라 `EventRecord` 계약과 queryable local lake다.

## 사용한 입력 근거

- 설명 문서
  - `README.md`
  - `problem/README.md`
  - `python/README.md`
  - `docs/README.md`
  - `docs/concepts/log-normalization.md`
- 구현
  - `python/src/cloudtrail_log_basics/etl.py`
  - `problem/data/cloudtrail_events.json`
  - `problem/data/vpc_flow_logs.json`
  - `.artifacts/log-basics.duckdb`
  - `.artifacts/log-basics.parquet`
- 테스트
  - `python/tests/test_etl.py`

## 다시 실행한 명령

```bash
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src \
  .venv/bin/python -m cloudtrail_log_basics.etl \
  00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json \
  00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json

PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src \
  .venv/bin/python -m pytest \
  00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

## 재실행 결과

- CLI 결과: `ingested 4 records`
- pytest 결과: `1 passed in 0.05s`
- `.artifacts/log-basics.parquet` 존재 확인

## 이번 재검증에서 추가로 확인한 사실

- `2026-03-14`에 CLI를 다시 돌린 뒤 `.artifacts/log-basics.duckdb`를 조회하자 event name별 count가 모두 `3`이었다.
- fixture 자체는 4건뿐인데 누적 count가 커진 이유는 `ingest_records()`가 `CREATE TABLE IF NOT EXISTS` 뒤에 append insert만 하기 때문이다.
- 반면 pytest는 `tmp_path` 아래 새 DuckDB 파일을 만들어 쓰므로 집계 결과가 각 이벤트당 `1`로 안정적으로 맞는다.
- 따라서 "테스트는 idempotent하지만 루트 `.artifacts` 데모 산출물은 누적형"이라는 해석은 소스와 `2026-03-14` 재실행 결과를 함께 본 source-based inference다.

## 단계별 근거

### 1. 서로 다른 로그를 같은 `EventRecord`로 정규화했다

- 근거 소스: `etl.py`, 두 fixture JSON
- 확인한 사실:
  - CloudTrail은 `eventTime`, `eventSource`, `eventName`, `userIdentity.arn`, `bucketName/userName`을 읽는다.
  - VPC Flow Logs는 `timestamp`, `source_ip`, `destination_port`, `interface_id`, `action`을 읽는다.
  - 두 경로 모두 `occurred_at`, `source`, `event_name`, `actor`, `resource_id`, `action_result`로 수렴한다.

### 2. 정규화 결과를 DuckDB와 Parquet에 동시에 남겼다

- 근거 소스: `ingest_records()`
- 확인한 사실:
  - `event_records` 테이블을 생성하고 insert한다.
  - 같은 내용을 `COPY ... FORMAT PARQUET`으로 parquet 파일로도 남긴다.
  - README가 DuckDB table과 Parquet를 공식 출력으로 문서화한다.

### 3. queryability를 테스트로 잠갔다

- 근거 소스: `test_etl.py`
- 확인한 사실:
  - event name summary는 `CreateAccessKey`, `PutBucketAcl`, `flow:22`, `flow:443`를 기대한다.
  - actor summary와 시간 범위 count도 함께 검증한다.
  - time window `2026-03-07T09:00:00Z` ~ `2026-03-07T09:05:00Z` 안에는 2건이 있어야 한다.

## 남은 한계

- `problem/README.md`가 말한 대로 전체 CloudTrail 스키마는 보존하지 않는다.
- 분산 적재와 대용량 파이프라인은 다루지 않는다.
- CLI 기본 경로 `.artifacts/log-basics.duckdb`는 append형이라 반복 시 데모 count가 누적된다. 이 문장은 `ingest_records()` 소스와 `2026-03-14` DuckDB 조회 결과를 함께 본 source-based inference다.

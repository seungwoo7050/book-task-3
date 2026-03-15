# 03 CloudTrail Log Basics: raw log를 저장하는 대신 queryable event로 눌러 놓은 첫 ETL

이 프로젝트가 하는 일은 로그를 많이 모으는 것이 아니다. `problem/README.md`가 요구하는 건 CloudTrail과 VPC Flow Logs를 이후 query와 detection이 재사용할 수 있는 가장 작은 공통 구조로 바꾸는 것이다. `2026-03-14`에 CLI, pytest, DuckDB 결과를 다시 확인해 보니, 이 lab의 핵심은 "정규화 -> 적재 -> 질의 검증"의 세 단계가 이미 다음 security lake를 위한 입력 계약처럼 작동한다는 점이었다. 반대로 루트 `.artifacts` 데모 산출물은 재실행마다 누적되어, 테스트와 데모 동작이 완전히 같지는 않았다.

## Step 1. 먼저 서로 다른 로그 두 개를 같은 `EventRecord`로 눌렀다

CloudTrail과 VPC Flow Logs는 원본 포맷이 다르다. 이 프로젝트는 그 차이를 없애려 하지 않고, 이후 분석에 필요한 최소 공통 필드만 뽑아 같은 dataclass에 담는다.

`etl.py`의 정규화 규칙은 명확하다.

- CloudTrail
  - `eventTime` -> `occurred_at`
  - `eventSource` -> `source`
  - `eventName` -> `event_name`
  - `userIdentity.arn` -> `actor`
  - `requestParameters.bucketName` 또는 `userName` -> `resource_id`
  - `action_result`는 `"cloudtrail"` 고정
- VPC Flow Logs
  - `timestamp` -> `occurred_at`
  - `source`는 `"vpc-flow-logs"` 고정
  - `destination_port` -> `event_name` (`flow:443` 같은 shape)
  - `source_ip` -> `actor`
  - `interface_id` -> `resource_id`
  - `action` -> `action_result`

즉 이 lab의 목표는 원본 로그를 모두 보존하는 게 아니라, 다음 단계가 같은 query를 던질 수 있는 공통 surface를 먼저 만드는 것이다. `docs/concepts/log-normalization.md`가 말하는 "원본 로그 포맷이 달라도 공통 필드를 정하면 이후 분석 코드가 단순해진다"는 문장은 바로 이 코드에서 실체를 얻는다.

## Step 2. 그 공통 레코드를 메모리에서 끝내지 않고 local lake 산출물로 남겼다

정규화만으로는 아직 ETL이 완성되지 않는다. `ingest_records()`는 정규화된 `EventRecord` 리스트를 DuckDB와 Parquet 두 군데에 동시에 남긴다.

```python
connection.execute(
    """
    CREATE TABLE IF NOT EXISTS event_records (
        occurred_at VARCHAR,
        source VARCHAR,
        event_name VARCHAR,
        actor VARCHAR,
        resource_id VARCHAR,
        action_result VARCHAR
    )
    """
)
connection.executemany(
    "INSERT INTO event_records VALUES (?, ?, ?, ?, ?, ?)",
    [tuple(asdict(record).values()) for record in records],
)
connection.execute(f"COPY event_records TO '{parquet_path}' (FORMAT PARQUET)")
```

이 설계 때문에 이 lab은 단순 parser가 아니라 작은 local lake를 만드는 단계가 된다.

- DuckDB: 바로 질의 가능한 로컬 분석 저장소
- Parquet: 다음 프로젝트가 다시 읽을 수 있는 전달용 산출물

`2026-03-14` CLI 재실행도 그 사실을 확인해 줬다.

```bash
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src \
  .venv/bin/python -m cloudtrail_log_basics.etl \
  00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json \
  00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
```

출력은 `ingested 4 records`였고, `.artifacts/log-basics.parquet`도 실제로 남아 있었다. 즉 "정규화했다"는 말이 메모리 안에서 끝나지 않고 파일 산출물까지 이어진다.

## Step 3. ETL의 성공 기준을 파일 존재가 아니라 query 결과로 잠갔다

이 프로젝트가 좋아 보이는 이유는 적재 이후를 테스트로 묶어 둔 데 있다. `test_etl.py`는 temporary DuckDB와 Parquet를 만들고, 단순 존재 여부를 넘어서 실제 집계 결과를 요구한다.

```python
assert summarize_by_event_name(db_path) == [
    ("CreateAccessKey", 1),
    ("PutBucketAcl", 1),
    ("flow:22", 1),
    ("flow:443", 1),
]
assert summarize_by_actor(db_path)[0][1] == 1
assert within_time_range(db_path, "2026-03-07T09:00:00Z", "2026-03-07T09:05:00Z") == 2
```

`2026-03-14` pytest 재실행 결과는 `1 passed in 0.05s`였다. 여기서 중요한 건 숫자보다 기준이다.

- event name summary가 정확히 네 종류여야 한다.
- actor summary가 queryable해야 한다.
- 특정 시간 범위 안 이벤트 수를 셀 수 있어야 한다.

즉 이 lab은 로그를 "적재 가능"하게 만든 것만이 아니라, 그 적재 결과가 바로 query 가능한 상태임을 테스트로 잠가 둔다.

## Step 4. 다만 CLI 기본 산출물은 idempotent하지 않다

이번 재검증에서 가장 중요한 추가 사실은 테스트와 데모 산출물이 완전히 같은 동작을 하지는 않는다는 점이었다. pytest는 `tmp_path` 아래 새 DB 파일을 만들기 때문에 항상 깨끗한 상태에서 시작한다. 반면 CLI 기본 경로는 루트 `.artifacts/log-basics.duckdb`를 계속 재사용한다.

`2026-03-14`에 CLI를 다시 돌린 뒤 DuckDB를 직접 조회하자 결과는 이랬다.

- `CreateAccessKey`: `3`
- `PutBucketAcl`: `3`
- `flow:22`: `3`
- `flow:443`: `3`
- 시간 범위 `2026-03-07T09:00:00Z` ~ `2026-03-07T09:05:00Z`: `6`

fixture는 분명 4건뿐인데 count가 커진 이유는 `ingest_records()`가 `CREATE TABLE IF NOT EXISTS` 후에 truncate 없이 `INSERT`만 하기 때문이다. 따라서 CLI는 "매번 새 lake를 만든다"기보다 "같은 local lake에 append한다"에 가깝다. 이 해석은 소스와 `2026-03-14` DuckDB 조회 결과를 함께 본 source-based inference다.

이건 꼭 나쁜 일만은 아니다. 반복 적재 데모에는 맞을 수 있다. 다만 README만 읽고 CLI를 여러 번 돌렸을 때 집계가 그대로 유지될 거라고 기대하면 실제 동작과 어긋난다. 그래서 이 현재 동작을 문서에 남겨 두는 편이 정확하다.

## 정리

`03-cloudtrail-log-basics`의 성취는 로그를 보기 좋게 바꾼 데 있지 않다. 서로 다른 raw log를 같은 `EventRecord` 계약으로 누르고, DuckDB + Parquet에 남기고, 그 결과를 집계 query로 검증했다는 데 있다. 그래서 다음 security lake 단계는 원본 포맷 처리보다 detection query 자체에 더 집중할 수 있다. 다만 루트 `.artifacts` CLI는 append형이라 반복 실행 시 count가 누적된다는 현재 성질도 함께 기억해 두는 편이 좋다.

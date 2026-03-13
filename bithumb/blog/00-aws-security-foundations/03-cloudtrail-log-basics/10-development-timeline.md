# 03 CloudTrail Log Basics: raw log를 queryable event로 바꾸는 ETL

원본 로그를 그대로 쌓는 대신, query와 detection이 가능한 공통 이벤트 구조로 바꾸는 가장 작은 ETL 단계다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "서로 다른 로그 포맷을 어떤 공통 필드로 눌러야 이후 query가 단순해지는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. CloudTrail과 VPC Flow Logs를 같은 `EventRecord` 필드 집합으로 정규화했다.
2. 정규화된 레코드를 DuckDB 테이블과 Parquet 산출물로 함께 적재했다.
3. 집계 쿼리와 기간 필터를 테스트에 넣어 ETL 결과가 실제 질의 가능한 상태임을 증명했다.

## Phase 1. 두 로그를 같은 EventRecord로 눌렀다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `두 로그를 같은 EventRecord로 눌렀다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: CloudTrail과 VPC Flow Logs를 하나의 분석 코드가 읽을 수 있는 공통 구조로 만든다.
- 변경 단위: `python/src/cloudtrail_log_basics/etl.py`의 `EventRecord`, `normalize_cloudtrail_events`, `normalize_vpc_flow_logs`
- 처음 가설: 포맷이 달라도 `occurred_at`, `source`, `event_name`, `actor`, `resource_id`를 공통으로 잡으면 이후 query는 훨씬 단순해진다.
- 실제 진행: CloudTrail에서는 `bucketName`이나 `userName` 같은 필드를 우선순위로 읽어 `resource_id`를 만들고, VPC Flow Logs에서는 `destination_port`를 `event_name`으로 올렸다. 결과적으로 서로 다른 로그가 같은 dataclass 배열 안에 들어가게 됐다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
```

검증 신호:
- CLI가 `ingested 4 records`를 출력했다.
- 두 입력 포맷이 한 번의 ETL 실행에서 함께 적재되는 경로가 생겼다.

핵심 코드:

```python
def normalize_cloudtrail_events(payload: dict[str, Any]) -> list[EventRecord]:
    records: list[EventRecord] = []
    for entry in payload.get("Records", []):
        resource_id = (
            entry.get("requestParameters", {}).get("bucketName")
            or entry.get("requestParameters", {}).get("userName")
            or "unknown"
        )
        records.append(
            EventRecord(
                occurred_at=str(entry["eventTime"]),
                source=str(entry["eventSource"]),
                event_name=str(entry["eventName"]),
                actor=str(entry.get("userIdentity", {}).get("arn", "unknown")),
                resource_id=str(resource_id),
                action_result="cloudtrail",
            )
        )
    return records


def normalize_vpc_flow_logs(entries: list[dict[str, Any]]) -> list[EventRecord]:
    records: list[EventRecord] = []
    for entry in entries:
        records.append(
            EventRecord(
                occurred_at=str(entry["timestamp"]),
                source="vpc-flow-logs",
                event_name=f"flow:{entry['destination_port']}",
                actor=str(entry["source_ip"]),
                resource_id=str(entry["interface_id"]),
                action_result=str(entry["action"]),
            )
        )
    return records
```

왜 이 코드가 중요했는가: 정규화 함수가 분리되면서 프로젝트의 핵심 질문이 분명해졌다. 원본 로그를 얼마나 많이 보존하느냐보다, 이후 분석에 필요한 공통 필드를 얼마나 정확히 뽑느냐가 중요해졌다.

새로 배운 것: 로그 정규화의 목표는 원본을 완벽히 보존하는 것이 아니라, 다음 단계가 공통 질의를 날릴 수 있는 shape를 만드는 것이다.

다음: 이제 공통 레코드를 실제 query engine에 적재하고 파일 산출물까지 남겨야 했다.

## Phase 2. DuckDB와 Parquet를 동시에 남겼다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `DuckDB와 Parquet를 동시에 남겼다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 정규화 결과를 로컬에서 즉시 질의 가능하고, 다음 프로젝트에도 넘길 수 있는 저장 구조로 만든다.
- 변경 단위: `python/src/cloudtrail_log_basics/etl.py`의 `ingest_records`
- 처음 가설: 메모리 배열로만 끝내면 security lake 감각이 오지 않는다. 로컬 DB와 columnar 파일을 같이 남겨야 다음 단계로 연결된다.
- 실제 진행: ETL은 `event_records` 테이블을 만들고, dataclass를 tuple로 바꿔 insert한 뒤, 같은 내용을 Parquet로 copy했다. 이 구성이 있어서 07번과 10번이 lake-like 산출물을 재활용할 수 있다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
```

검증 신호:
- `ingested 4 records` 출력 뒤 `.artifacts/log-basics.parquet`가 생긴다.
- README가 DuckDB table과 Parquet 산출물을 공식 출력으로 문서화하고 있다.

핵심 코드:

```python
def ingest_records(records: list[EventRecord], db_path: Path, parquet_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(db_path))
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

왜 이 코드가 중요했는가: 이 블록이 생기면서 프로젝트는 단순 parser에서 ETL로 성격이 바뀌었다. 분석 대상이 메모리 안에서 사라지지 않고, queryable storage에 남기 때문이다.

새로 배운 것: DuckDB + Parquet 조합은 로컬 학습에서도 security lake 사고방식을 체험하기에 충분하다. DB는 질의용, Parquet는 전달 가능한 산출물 역할을 한다.

다음: 적재만으로는 부족하니, 실제 집계와 기간 질의를 테스트에 넣어 ETL의 효용을 증명해야 했다.

## Phase 3. 집계 쿼리와 time range를 테스트로 잠갔다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `집계 쿼리와 time range를 테스트로 잠갔다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 적재 결과가 정말 queryable한지 확인한다.
- 변경 단위: `python/src/cloudtrail_log_basics/etl.py`의 summary 함수들, `python/tests/test_etl.py`
- 처음 가설: ETL이 제대로 됐다는 말은 파일이 생겼다는 뜻이 아니라, event name/actor/time range 질의가 의도한 결과를 돌려준다는 뜻이다.
- 실제 진행: `summarize_by_event_name`, `summarize_by_actor`, `within_time_range`를 추가해 실제 질의 경로를 만들고, 테스트는 4개의 이벤트가 어떤 이름과 기간으로 집계되는지 구체적으로 고정했다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

검증 신호:
- pytest가 `1 passed in 0.13s`로 통과했다.
- 테스트는 `CreateAccessKey`, `PutBucketAcl`, `flow:22`, `flow:443` 집계와 2건의 기간 내 이벤트를 정확히 요구했다.

핵심 코드:

```python
def test_etl_ingests_cloudtrail_and_vpc_flow_logs(tmp_path: Path) -> None:
    cloudtrail = json.loads(_problem_data("cloudtrail_events.json").read_text())
    vpc_flow = json.loads(_problem_data("vpc_flow_logs.json").read_text())
    records = normalize_cloudtrail_events(cloudtrail) + normalize_vpc_flow_logs(vpc_flow)

    db_path = tmp_path / "events.duckdb"
    parquet_path = tmp_path / "events.parquet"
    ingest_records(records, db_path, parquet_path)

    assert parquet_path.exists()
    assert summarize_by_event_name(db_path) == [
        ("CreateAccessKey", 1),
        ("PutBucketAcl", 1),
        ("flow:22", 1),
        ("flow:443", 1),
    ]
    assert summarize_by_actor(db_path)[0][1] == 1
    assert within_time_range(db_path, "2026-03-07T09:00:00Z", "2026-03-07T09:05:00Z") == 2
```

왜 이 코드가 중요했는가: 이 테스트가 들어가면서 ETL은 추상적인 “적재했다”에서 벗어나, 어떤 분석 질문에 답할 수 있는지가 구체적으로 드러났다.

새로 배운 것: 정규화의 성공은 raw schema 보존이 아니라, 필요한 질문을 얼마나 짧은 query로 풀 수 있느냐로 판단하는 편이 좋다.

다음: 다음 프로젝트는 이 감각을 한 단계 밀어, 적재된 이벤트 위에서 탐지 쿼리를 직접 돌린다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 프로젝트는 log parsing보다 한 단계 더 앞서 있었다. 공통 이벤트 구조를 세우고, DuckDB/Parquet에 남기고, 집계 쿼리로 검증하는 순서를 밟았기 때문에 07번 security lake와 10번 capstone이 같은 입력 감각을 이어받을 수 있었다.

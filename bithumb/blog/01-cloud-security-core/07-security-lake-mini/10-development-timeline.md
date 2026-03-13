# 07 Security Lake Mini: local lake에서 detection query를 굴리기

CloudTrail fixture를 local lake에 적재하고 preset detection query로 alert를 만드는 최소 security lake 실습이다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "security lake를 로컬로 축소할 때 무엇을 먼저 고정해야 하는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. CloudTrail fixture를 DuckDB 테이블과 Parquet 파일로 적재했다.
2. preset SQL query가 `LAKE-*` control을 순서대로 만들게 했다.
3. CLI가 적재와 탐지를 한 번에 실행하고, 테스트가 alert 순서를 고정했다.

## Phase 1. CloudTrail fixture를 local lake로 적재했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `CloudTrail fixture를 local lake로 적재했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: CloudTrail 이벤트를 DuckDB/Parquet lake 산출물로 바꾼다.
- 변경 단위: `python/src/security_lake_mini/lake.py`의 `_normalize`, `ingest_cloudtrail`
- 처음 가설: security lake를 설명하려면 먼저 로그가 질의 가능한 저장 구조 안에 있어야 한다.
- 실제 진행: fixture의 `Records`를 순회해 `(occurred_at, source, event_name, actor)` 행으로 정규화하고, `lake_events` 테이블과 Parquet 파일에 동시에 적재했다. 이 과정에서 테이블은 매번 비우고 다시 채워 local demo 반복성을 높였다.

CLI:

```bash
$ mkdir -p .artifacts/security-lake-mini
$ PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
```

검증 신호:
- CLI 실행 후 `lake.duckdb`와 `events.parquet` 경로가 채워졌다.
- README는 이 경로들을 명시적 입력/출력으로 노출한다.

핵심 코드:

```python
def ingest_cloudtrail(cloudtrail_path: Path, db_path: Path, parquet_path: Path) -> None:
    payload = json.loads(cloudtrail_path.read_text())
    rows = _normalize(payload)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect(str(db_path))
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS lake_events (
            occurred_at VARCHAR,
            source VARCHAR,
            event_name VARCHAR,
            actor VARCHAR
        )
        """
    )
    connection.execute("DELETE FROM lake_events")
    connection.executemany("INSERT INTO lake_events VALUES (?, ?, ?, ?)", rows)
    connection.execute(f"COPY lake_events TO '{parquet_path}' (FORMAT PARQUET)")
```

왜 이 코드가 중요했는가: lake라는 말을 코드 수준에서 실체화하는 블록이 바로 여기였다. 로그를 그냥 메모리에서 스캔하는 게 아니라, 쿼리 가능한 저장 구조에 넣는다.

새로 배운 것: security lake는 로그 저장소가 아니라, 탐지 쿼리가 반복 실행될 수 있는 저장 계층이다.

다음: 적재만으로는 lake가 완성되지 않으니, preset detection query를 붙여 alert를 만들어야 했다.

## Phase 2. SQL query를 alert taxonomy로 썼다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `SQL query를 alert taxonomy로 썼다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 이벤트 이름 기반의 suspicious activity를 `LAKE-*` control로 매핑한다.
- 변경 단위: `python/src/security_lake_mini/lake.py`의 `run_detection_queries`
- 처음 가설: query preset이 있어야 “이 lake에서 뭘 찾는가”를 즉시 설명할 수 있다.
- 실제 진행: `CASE` 문으로 `CreateAccessKey`, `PutBucketAcl`, `AuthorizeSecurityGroupIngress`, `DeleteTrail`, root `ConsoleLogin`을 각각 `LAKE-001`부터 `LAKE-005`로 매핑했다. 그 결과 rowset이 alert dataclass 배열로 다시 올라왔다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
```

검증 신호:
- 실제 CLI 출력에 `LAKE-001`부터 `LAKE-005`까지 다섯 개 alert가 순서대로 나타났다.
- 각 alert는 `event_name`, `actor`, `occurred_at`를 그대로 포함해 설명 가능한 형태가 됐다.

핵심 코드:

```python
def run_detection_queries(db_path: Path) -> list[Alert]:
    connection = duckdb.connect(str(db_path))
    query = """
    SELECT
      CASE
        WHEN event_name = 'CreateAccessKey' THEN 'LAKE-001'
        WHEN event_name = 'PutBucketAcl' THEN 'LAKE-002'
        WHEN event_name = 'AuthorizeSecurityGroupIngress' THEN 'LAKE-003'
        WHEN event_name = 'DeleteTrail' THEN 'LAKE-004'
        WHEN event_name = 'ConsoleLogin' AND actor LIKE '%:root' THEN 'LAKE-005'
        ELSE 'INFO'
      END AS control_id,
      event_name,
      actor,
      occurred_at
    FROM lake_events
    WHERE event_name IN (
      'CreateAccessKey',
      'PutBucketAcl',
      'AuthorizeSecurityGroupIngress',
      'DeleteTrail',
      'ConsoleLogin'
    )
    ORDER BY occurred_at
    """
    alerts: list[Alert] = []
    for control_id, event_name, actor, occurred_at in connection.execute(query).fetchall():
        alerts.append(
            Alert(
                control_id=str(control_id),
                title=f"Detected suspicious event: {event_name}",
                event_name=str(event_name),
                actor=str(actor),
                occurred_at=str(occurred_at),
            )
        )
    return alerts
```

왜 이 코드가 중요했는가: 이 쿼리가 들어오면서 프로젝트는 단순 ingestion demo에서 detection engineering demo로 바뀌었다. 어떤 이벤트를 이상행위 예시로 볼지 taxonomy가 생겼기 때문이다.

새로 배운 것: 좋은 detection preset은 “왜 잡혔는가”를 event_name 수준에서 바로 설명할 수 있어야 한다. query가 taxonomy 역할을 한다.

다음: 이제 적재와 탐지를 한 번에 묶고, alert 순서를 테스트로 고정해야 했다.

## Phase 3. CLI와 테스트로 alert 순서를 잠갔다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `CLI와 테스트로 alert 순서를 잠갔다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 로컬에서 같은 입력을 주면 같은 alert 집합이 재현되게 한다.
- 변경 단위: `python/src/security_lake_mini/cli.py`, `python/tests/test_lake.py`
- 처음 가설: detection demo는 결과가 존재하는 것만으로 부족하다. 어떤 순서와 control set이 나와야 하는지도 고정돼야 한다.
- 실제 진행: CLI는 ingest 직후 `run_detection_queries`를 실행해 JSON alert 목록을 반환하게 했고, 테스트는 Parquet 파일 생성과 `LAKE-001`~`LAKE-005` 순서를 정확히 요구했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

검증 신호:
- pytest가 `2 passed in 0.16s`로 통과했다.
- `test_security_lake_generates_expected_alerts`가 control_id 배열의 순서를 그대로 비교한다.

핵심 코드:

```python
def test_security_lake_generates_expected_alerts(tmp_path: Path) -> None:
    cloudtrail = Path(__file__).resolve().parents[2] / "problem" / "data" / "cloudtrail_suspicious.json"
    db_path = tmp_path / "lake.duckdb"
    parquet_path = tmp_path / "lake.parquet"

    ingest_cloudtrail(cloudtrail, db_path, parquet_path)
    alerts = run_detection_queries(db_path)

    assert parquet_path.exists()
    assert [alert.control_id for alert in alerts] == [
        "LAKE-001",
        "LAKE-002",
        "LAKE-003",
        "LAKE-004",
        "LAKE-005",
    ]
```

왜 이 코드가 중요했는가: 이 테스트가 alert 순서까지 잠그면서, 프로젝트는 “뭔가 탐지된다”가 아니라 “이 fixture에서 무엇이 어떤 순서로 탐지돼야 하는가”를 명시하게 됐다.

새로 배운 것: detection demo에서는 alert 존재 여부보다 rule taxonomy와 ordering을 고정하는 편이 회귀를 잡기 쉽다.

다음: 다음 프로젝트는 로그 대신 manifest와 image metadata를 대상으로 guardrail scanner를 만든다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

local security lake라는 말이 추상적으로 들리지 않는 이유는, 이 프로젝트가 적재와 detection query를 같은 CLI 흐름 안에 묶어 두었기 때문이다. 그래서 capstone에서도 CloudTrail ingestion이 곧 finding 생성으로 이어지는 구조를 자연스럽게 설명할 수 있었다.

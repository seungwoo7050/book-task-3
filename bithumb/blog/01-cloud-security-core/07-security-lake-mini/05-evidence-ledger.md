# 07 Security Lake Mini 근거 정리

이 문서는 "CloudTrail을 lake에 넣었다"는 요약보다, 어떤 코드와 어떤 재실행 결과 때문에 그렇게 말할 수 있는지를 고정하는 메모다. 이번 lab은 코드가 짧은 대신, 작은 함수 하나가 의미를 크게 바꾸는 지점이 많아서 그 차이를 분리해서 적는 게 중요했다.

## Phase 1. 적재 단계가 lake의 최소 shape를 고정한다

- 당시 목표: fixture 로그를 질의 가능한 local lake row로 바꾼다.
- 핵심 근거:
  - `_normalize()`는 `Records`를 `(occurred_at, source, event_name, actor)` 4열 row로 바꾼다.
  - `userIdentity.arn`이 없으면 actor는 `"unknown"`으로 들어간다.
  - `ingest_cloudtrail()`은 `CREATE TABLE IF NOT EXISTS lake_events` 뒤에 `DELETE FROM lake_events`를 수행하고 다시 insert 한다.
  - 같은 함수가 Parquet export도 함께 수행한다.
- 재실행:
  - `mkdir -p /Users/woopinbell/work/book-task-3/bithumb/.artifacts/security-lake-mini`
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m security_lake_mini.cli /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json /Users/woopinbell/work/book-task-3/bithumb/.artifacts/security-lake-mini/lake.duckdb /Users/woopinbell/work/book-task-3/bithumb/.artifacts/security-lake-mini/events.parquet`
- 검증 신호:
  - CLI가 `LAKE-001`부터 `LAKE-005`까지 5개 alert를 출력했다.
  - 별도 DuckDB 조회에서 `select count(*) from lake_events` 결과가 `5`였다.
  - 같은 조회에서 event 순서는 fixture chronology와 동일했다.
- 해석:
  - 이 lab은 lake를 "파일을 쌓아 두는 곳"이 아니라, rerun마다 같은 query를 태울 수 있는 resettable row store로 다룬다.

## Phase 2. alert taxonomy는 SQL query 안에서 고정된다

- 당시 목표: suspicious activity 예시를 사람이 바로 읽을 수 있는 control ID 목록으로 바꾼다.
- 핵심 근거:
  - `run_detection_queries()`는 `CASE` 문으로 다섯 event를 `LAKE-001`~`LAKE-005`에 매핑한다.
  - `ConsoleLogin`은 actor가 `%:root`일 때만 `LAKE-005`가 된다.
  - 반환 title은 모두 `Detected suspicious event: <event_name>` 형식이다.
  - `eventSource`는 lake row에 저장되지만 detection query에서는 쓰이지 않는다.
- 재실행:
  - CLI 출력과 별도 DuckDB SQL 재조회로 control 순서를 다시 확인했다.
- 검증 신호:
  - control 순서는 `LAKE-001`, `LAKE-002`, `LAKE-003`, `LAKE-004`, `LAKE-005`
  - 대응 event는 각각 `CreateAccessKey`, `PutBucketAcl`, `AuthorizeSecurityGroupIngress`, `DeleteTrail`, root `ConsoleLogin`
- 해석:
  - 이 프로젝트의 taxonomy는 외부 rule registry가 아니라 SQL query 그 자체에 박혀 있다.
- source-based inference:
  - `CASE`에는 `ELSE 'INFO'`가 있지만, 바로 아래 `WHERE event_name IN (...)`가 같은 다섯 event만 허용하므로 현재 쿼리 결과에서 `INFO`는 사실상 나오지 않는다.

## Phase 3. CLI와 테스트가 rerun 가능성을 잠근다

- 당시 목표: 로컬에서 같은 입력을 주면 같은 lake와 같은 alert 배열이 반복 재생산되게 한다.
- 핵심 근거:
  - CLI는 ingest 직후 `run_detection_queries(db_path)`를 호출해 JSON 배열을 출력한다.
  - `test_security_lake_generates_expected_alerts()`는 Parquet 생성과 control 순서를 둘 다 확인한다.
  - `test_cli_ingest_returns_json_alerts()`는 CLI stdout에 `LAKE-001`이 포함되는지와 Parquet 생성 여부를 본다.
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m pytest /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python/tests`
- 검증 신호:
  - `2 passed in 0.07s`
- 해석:
  - 이 lab이 보장하는 것은 "lake가 있다"가 아니라, 같은 fixture가 같은 control array로 재현된다는 점이다.

## 이번 Todo에서 남긴 한계

- detection은 단일 테이블, 단일 SQL에 고정돼 있다.
- `eventSource`는 저장되지만 현재 detection에서는 unused field다.
- `INFO` branch는 query 구조상 도달하지 않는다.
- severity, suppression, windowed correlation 같은 운영형 detection 요소는 아직 없다.

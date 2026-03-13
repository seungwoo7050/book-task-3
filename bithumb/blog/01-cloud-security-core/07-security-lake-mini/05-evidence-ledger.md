# 07 Security Lake Mini 근거 정리

CloudTrail fixture를 local lake에 적재하고 preset detection query로 alert를 만드는 최소 security lake 실습이다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. CloudTrail fixture를 local lake로 적재했다

이 구간에서는 `CloudTrail fixture를 local lake로 적재했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: CloudTrail 이벤트를 DuckDB/Parquet lake 산출물로 바꾼다.
- 변경 단위: `python/src/security_lake_mini/lake.py`의 `_normalize`, `ingest_cloudtrail`
- 처음 가설: security lake를 설명하려면 먼저 로그가 질의 가능한 저장 구조 안에 있어야 한다.
- 실제 조치: fixture의 `Records`를 순회해 `(occurred_at, source, event_name, actor)` 행으로 정규화하고, `lake_events` 테이블과 Parquet 파일에 동시에 적재했다. 이 과정에서 테이블은 매번 비우고 다시 채워 local demo 반복성을 높였다.
- CLI:
  - `mkdir -p .artifacts/security-lake-mini`
  - `PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet`
- 검증 신호:
  - CLI 실행 후 `lake.duckdb`와 `events.parquet` 경로가 채워졌다.
  - README는 이 경로들을 명시적 입력/출력으로 노출한다.
- 핵심 코드 앵커: `01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py:37-56`
- 새로 배운 것: security lake는 로그 저장소가 아니라, 탐지 쿼리가 반복 실행될 수 있는 저장 계층이다.
- 다음: 적재만으로는 lake가 완성되지 않으니, preset detection query를 붙여 alert를 만들어야 했다.

## Phase 2. SQL query를 alert taxonomy로 썼다

이 구간에서는 `SQL query를 alert taxonomy로 썼다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: 이벤트 이름 기반의 suspicious activity를 `LAKE-*` control로 매핑한다.
- 변경 단위: `python/src/security_lake_mini/lake.py`의 `run_detection_queries`
- 처음 가설: query preset이 있어야 “이 lake에서 뭘 찾는가”를 즉시 설명할 수 있다.
- 실제 조치: `CASE` 문으로 `CreateAccessKey`, `PutBucketAcl`, `AuthorizeSecurityGroupIngress`, `DeleteTrail`, root `ConsoleLogin`을 각각 `LAKE-001`부터 `LAKE-005`로 매핑했다. 그 결과 rowset이 alert dataclass 배열로 다시 올라왔다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet`
- 검증 신호:
  - 실제 CLI 출력에 `LAKE-001`부터 `LAKE-005`까지 다섯 개 alert가 순서대로 나타났다.
  - 각 alert는 `event_name`, `actor`, `occurred_at`를 그대로 포함해 설명 가능한 형태가 됐다.
- 핵심 코드 앵커: `01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py:59-95`
- 새로 배운 것: 좋은 detection preset은 “왜 잡혔는가”를 event_name 수준에서 바로 설명할 수 있어야 한다. query가 taxonomy 역할을 한다.
- 다음: 이제 적재와 탐지를 한 번에 묶고, alert 순서를 테스트로 고정해야 했다.

## Phase 3. CLI와 테스트로 alert 순서를 잠갔다

이 구간에서는 `CLI와 테스트로 alert 순서를 잠갔다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 로컬에서 같은 입력을 주면 같은 alert 집합이 재현되게 한다.
- 변경 단위: `python/src/security_lake_mini/cli.py`, `python/tests/test_lake.py`
- 처음 가설: detection demo는 결과가 존재하는 것만으로 부족하다. 어떤 순서와 control set이 나와야 하는지도 고정돼야 한다.
- 실제 조치: CLI는 ingest 직후 `run_detection_queries`를 실행해 JSON alert 목록을 반환하게 했고, 테스트는 Parquet 파일 생성과 `LAKE-001`~`LAKE-005` 순서를 정확히 요구했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests`
- 검증 신호:
  - pytest가 `2 passed in 0.16s`로 통과했다.
  - `test_security_lake_generates_expected_alerts`가 control_id 배열의 순서를 그대로 비교한다.
- 핵심 코드 앵커: `01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py:6-21`
- 새로 배운 것: detection demo에서는 alert 존재 여부보다 rule taxonomy와 ordering을 고정하는 편이 회귀를 잡기 쉽다.
- 다음: 다음 프로젝트는 로그 대신 manifest와 image metadata를 대상으로 guardrail scanner를 만든다.

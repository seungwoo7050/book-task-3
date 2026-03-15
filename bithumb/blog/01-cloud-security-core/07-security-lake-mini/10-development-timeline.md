# 07 Security Lake Mini: 저장보다 중요한 것은 같은 쿼리를 다시 돌릴 수 있는가

이 lab은 security lake를 거창한 분산 저장소로 설명하지 않는다. 대신 CloudTrail fixture 몇 개를 로컬 DuckDB에 넣고, preset detection query를 돌려 같은 alert taxonomy를 반복해서 얻는 흐름을 만든다. 그래서 chronology도 "얼마나 큰 lake를 만들었는가"가 아니라, "어떻게 같은 입력에서 같은 alert를 다시 만들 수 있게 했는가"를 따라가는 편이 맞다.

## 구현 순서 요약
1. CloudTrail fixture를 4열 row로 정규화해 DuckDB와 Parquet에 적재했다.
2. SQL query 하나에 `LAKE-001`부터 `LAKE-005` taxonomy를 심었다.
3. CLI와 테스트로 같은 입력에서 같은 alert 배열이 나오도록 잠갔다.

## Phase 1. 적재를 append가 아니라 reset 가능 상태로 만들었다

`ingest_cloudtrail()`를 보면 이 lab이 무엇을 lake라고 부르는지 바로 드러난다. 입력 JSON의 `Records`를 순회해 `(occurred_at, source, event_name, actor)` row로 바꾸고, `lake_events` 테이블에 넣는다. 여기서 눈에 띄는 부분은 `DELETE FROM lake_events`다. 이전 실습처럼 누적 append를 보여 주는 게 아니라, rerun할 때 같은 lake 상태를 다시 만들려는 선택이다.

이 덕분에 로컬 데모는 안정적이다. 같은 fixture를 다시 넣어도 row가 중복으로 쌓이지 않는다. 이번 재실행에서도 CLI를 돌린 뒤 DuckDB를 직접 열어 보니 `lake_events` row 수는 `5`로 유지됐고, event 순서도 fixture와 똑같이 남아 있었다.

재실행:

```bash
mkdir -p /Users/woopinbell/work/book-task-3/bithumb/.artifacts/security-lake-mini
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m security_lake_mini.cli \
/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json \
/Users/woopinbell/work/book-task-3/bithumb/.artifacts/security-lake-mini/lake.duckdb \
/Users/woopinbell/work/book-task-3/bithumb/.artifacts/security-lake-mini/events.parquet
```

보조 확인:
- `select count(*) from lake_events` 결과는 `5`
- event 순서는 `CreateAccessKey -> PutBucketAcl -> AuthorizeSecurityGroupIngress -> DeleteTrail -> ConsoleLogin`

여기서 중요한 건 Parquet를 만든 사실 자체보다, 같은 lake 상태를 계속 재생산할 수 있게 했다는 점이다.

## Phase 2. alert taxonomy는 SQL query가 직접 들고 있다

다음 단계는 "무엇을 찾을 것인가"를 고정하는 일이다. `run_detection_queries()`는 별도 rules engine을 두지 않고, SQL `CASE` 문 안에 detection taxonomy를 직접 적어 둔다. `CreateAccessKey`는 `LAKE-001`, `PutBucketAcl`은 `LAKE-002`, `AuthorizeSecurityGroupIngress`는 `LAKE-003`, `DeleteTrail`은 `LAKE-004`, 그리고 root actor의 `ConsoleLogin`만 `LAKE-005`가 된다.

이 구현에서 흥미로운 점은 저장된 컬럼과 실제 탐지 신호가 완전히 같지 않다는 것이다. row에는 `source`도 남기지만, 현재 detection은 거의 전부 `event_name`과 actor 문자열에 의존한다. 즉, lake schema는 조금 더 넓고, rule set은 그보다 좁다. 또 `CASE`에 `ELSE 'INFO'`가 있긴 하지만 바로 뒤 `WHERE event_name IN (...)`가 같은 다섯 event만 허용하므로, 현재 쿼리에서 `INFO`는 실제로 나오지 않는다.

이번 재실행의 CLI 출력은 아래 순서로 나왔다.

- `LAKE-001` / `CreateAccessKey`
- `LAKE-002` / `PutBucketAcl`
- `LAKE-003` / `AuthorizeSecurityGroupIngress`
- `LAKE-004` / `DeleteTrail`
- `LAKE-005` / `ConsoleLogin` with `arn:aws:iam::123456789012:root`

즉 이 lab에서 taxonomy는 문서가 아니라 SQL에 박혀 있는 셈이다.

## Phase 3. CLI와 테스트가 "같은 입력이면 같은 결과"를 보장한다

마지막으로 본 것은 재현성이다. CLI는 ingest와 detection을 따로 두지 않는다. 입력 path, DB path, Parquet path를 받아 적재를 끝내자마자 detection query를 돌리고 JSON alert 배열을 뱉는다. 이 구조는 학습용으로 꽤 중요하다. 저장 계층과 탐지 계층을 분리해서 설명하되, 반복 실험은 한 커맨드로 끝낼 수 있기 때문이다.

테스트도 같은 방향을 강화한다. `test_security_lake_generates_expected_alerts()`는 단순히 alert가 존재하는지만 보지 않고, `LAKE-001`부터 `LAKE-005`까지 control 순서를 배열 그대로 비교한다. `test_cli_ingest_returns_json_alerts()`는 CLI 출력에 `LAKE-001`이 들어 있는지와 Parquet가 실제 생성됐는지를 함께 확인한다.

재실행:

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m pytest \
/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python/tests
```

확인한 출력:

```text
..                                                                       [100%]
2 passed in 0.07s
```

이 테스트 셋은 작은 만큼 솔직하다. 복잡한 correlation이나 time window는 없지만, 적어도 "fixture 하나를 넣었을 때 어떤 suspicious event set가 어떤 순서로 나와야 하는가"는 분명히 고정한다.

## 지금 상태에서 분명한 한계

- detection은 단일 `lake_events` 테이블만 사용한다.
- `source` 컬럼은 저장되지만 현재 rule에서는 쓰이지 않는다.
- severity, suppression, deduplication, correlation window는 없다.
- root login 판단은 actor 문자열 suffix에 의존한다.

그래도 이 lab이 의미 있는 이유는 분명하다. security lake를 저장 기술로 풀지 않고, "같은 로그를 넣었을 때 같은 쿼리와 같은 alert taxonomy를 반복 실행할 수 있는가"라는 관점으로 축소해 보여 주기 때문이다. capstone으로 넘어갈 때 필요한 감각도 바로 여기서 만들어진다.

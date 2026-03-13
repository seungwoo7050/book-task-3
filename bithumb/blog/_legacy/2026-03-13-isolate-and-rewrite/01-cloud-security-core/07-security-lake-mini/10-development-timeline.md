# 10 Development Timeline

이 문서는 `Security Lake Mini`를 현재 CloudTrail fixture, lake 코드, CLI 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 generic lakehouse 실험이 아니라, 작은 detection query 세트를 반복 실행하는 local security lake인지 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `lake.py`, `test_lake.py`, `test_cli.py`를 함께 읽었다.
- 이슈: 처음엔 여러 테이블 join이나 상관 분석이 있을 거라 생각했는데, 실제 구현은 `lake_events` 단일 테이블과 `CASE` 기반 control ID 매핑에 집중하고 있었다.
- 판단: 이 프로젝트의 핵심은 복잡한 저장 구조가 아니라, 적재된 로그를 다시 읽어 alert를 생성하는 최소 loop를 코드로 고정하는 데 있다.

CLI:

```bash
$ sed -n '1,120p' 01-cloud-security-core/07-security-lake-mini/problem/README.md
$ sed -n '1,260p' 01-cloud-security-core/07-security-lake-mini/python/src/security_lake_mini/lake.py
$ sed -n '1,200p' 01-cloud-security-core/07-security-lake-mini/python/tests/test_lake.py
$ sed -n '1,200p' 01-cloud-security-core/07-security-lake-mini/python/tests/test_cli.py
```

이 시점의 핵심 코드는 event name을 `LAKE-*` control ID로 직접 매핑하는 query였다.

```sql
CASE
  WHEN event_name = 'CreateAccessKey' THEN 'LAKE-001'
  WHEN event_name = 'PutBucketAcl' THEN 'LAKE-002'
  WHEN event_name = 'AuthorizeSecurityGroupIngress' THEN 'LAKE-003'
  WHEN event_name = 'DeleteTrail' THEN 'LAKE-004'
  WHEN event_name = 'ConsoleLogin' AND actor LIKE '%:root' THEN 'LAKE-005'
END
```

처음엔 별도 규칙 엔진 객체가 필요하다고 생각했지만, 이 프로젝트 범위에서는 SQL 한 덩어리로 보는 편이 “어떤 이벤트가 어떤 alert가 되는가”를 더 직접적으로 보여 준다. 나중에 보니 이 단순함이 CLI와 테스트를 같이 유지하기도 더 쉬웠다.

### Session 2

- 진행: CLI와 pytest를 다시 돌려 적재와 detection이 한 번에 재현되는지 확인했다.
- 검증: CLI는 `LAKE-001`부터 `LAKE-005`까지 다섯 alert를 순서대로 출력했고, pytest는 lake test와 CLI test 두 경로를 모두 통과했다.
- 판단: 처음 가설은 적재 성공만 확인하면 된다는 쪽이었지만, `test_cli_ingest_returns_json_alerts()`가 있어야 사용자가 db/parquet 경로를 직접 줬을 때도 결과 형식이 흔들리지 않는다.
- 다음: 10번 capstone의 CloudTrail ingestion은 여기서의 적재 감각을 더 좁게 가져가고, finding 저장은 별도 DB 레이어에서 맡는다.

CLI:

```bash
$ make venv
$ mkdir -p .artifacts/security-lake-mini
$ PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m security_lake_mini.cli 01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json .artifacts/security-lake-mini/lake.duckdb .artifacts/security-lake-mini/events.parquet
$ PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
```

출력:

```text
"control_id": "LAKE-001"
"control_id": "LAKE-005"
2 passed in 0.08s
```

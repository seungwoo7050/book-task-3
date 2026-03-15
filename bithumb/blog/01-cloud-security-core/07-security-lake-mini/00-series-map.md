# 07 Security Lake Mini 읽기 지도

이 lab은 "로그를 저장했다"에서 멈추지 않고, 로컬 DuckDB 위에서 preset detection query까지 반복 실행하는 가장 작은 security lake 실습이다. 읽을 때도 저장소 이야기보다 `정규화 -> 적재 -> 쿼리 -> alert taxonomy` 흐름을 먼저 붙드는 편이 훨씬 정확하다.

## 먼저 붙들 질문
- local lake라고 부르기 위해 최소한 무엇이 있어야 하는가?
- 이 프로젝트의 alert taxonomy는 어디서 정의되는가?
- 왜 테스트가 alert 개수만이 아니라 순서까지 잠그고 있는가?

## 이 글은 이렇게 읽으면 된다
1. `_normalize()`와 `ingest_cloudtrail()`을 먼저 본다. CloudTrail fixture가 어떤 row shape로 lake에 들어가는지 확인한다.
2. `run_detection_queries()`를 본다. `LAKE-001`부터 `LAKE-005`까지가 어디서 정해지는지 확인한다.
3. 마지막으로 CLI와 테스트를 본다. 같은 입력을 여러 번 줘도 같은 lake와 같은 alert 순서가 나오는지 확인한다.

## 특히 눈여겨볼 장면
- 적재 단계가 DuckDB와 Parquet를 동시에 만들지만, 탐지 쿼리는 DuckDB `lake_events`만 읽는다.
- `DELETE FROM lake_events`가 들어 있어서 rerun이 append가 아니라 reset 기반으로 동작한다.
- detection taxonomy는 `eventSource`보다 `event_name`과 root actor 문자열 조건에 더 크게 의존한다.
- `CASE ... ELSE 'INFO'` branch는 있어도 현재 `WHERE event_name IN (...)` 때문에 실제 결과에는 나오지 않는다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md)

## 이번 문서의 근거
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/lake-thinking.md`
- `problem/data/cloudtrail_suspicious.json`
- `python/src/security_lake_mini/lake.py`
- `python/src/security_lake_mini/cli.py`
- `python/tests/test_lake.py`
- `python/tests/test_cli.py`

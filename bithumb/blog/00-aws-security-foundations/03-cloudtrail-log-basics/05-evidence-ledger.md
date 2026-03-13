# 03 CloudTrail Log Basics 근거 정리

원본 로그를 그대로 쌓는 대신, query와 detection이 가능한 공통 이벤트 구조로 바꾸는 가장 작은 ETL 단계다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. 두 로그를 같은 EventRecord로 눌렀다

이 구간에서는 `두 로그를 같은 EventRecord로 눌렀다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: CloudTrail과 VPC Flow Logs를 하나의 분석 코드가 읽을 수 있는 공통 구조로 만든다.
- 변경 단위: `python/src/cloudtrail_log_basics/etl.py`의 `EventRecord`, `normalize_cloudtrail_events`, `normalize_vpc_flow_logs`
- 처음 가설: 포맷이 달라도 `occurred_at`, `source`, `event_name`, `actor`, `resource_id`를 공통으로 잡으면 이후 query는 훨씬 단순해진다.
- 실제 조치: CloudTrail에서는 `bucketName`이나 `userName` 같은 필드를 우선순위로 읽어 `resource_id`를 만들고, VPC Flow Logs에서는 `destination_port`를 `event_name`으로 올렸다. 결과적으로 서로 다른 로그가 같은 dataclass 배열 안에 들어가게 됐다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json`
- 검증 신호:
  - CLI가 `ingested 4 records`를 출력했다.
  - 두 입력 포맷이 한 번의 ETL 실행에서 함께 적재되는 경로가 생겼다.
- 핵심 코드 앵커: `00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py:21-55`
- 새로 배운 것: 로그 정규화의 목표는 원본을 완벽히 보존하는 것이 아니라, 다음 단계가 공통 질의를 날릴 수 있는 shape를 만드는 것이다.
- 다음: 이제 공통 레코드를 실제 query engine에 적재하고 파일 산출물까지 남겨야 했다.

## Phase 2. DuckDB와 Parquet를 동시에 남겼다

이 구간에서는 `DuckDB와 Parquet를 동시에 남겼다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: 정규화 결과를 로컬에서 즉시 질의 가능하고, 다음 프로젝트에도 넘길 수 있는 저장 구조로 만든다.
- 변경 단위: `python/src/cloudtrail_log_basics/etl.py`의 `ingest_records`
- 처음 가설: 메모리 배열로만 끝내면 security lake 감각이 오지 않는다. 로컬 DB와 columnar 파일을 같이 남겨야 다음 단계로 연결된다.
- 실제 조치: ETL은 `event_records` 테이블을 만들고, dataclass를 tuple로 바꿔 insert한 뒤, 같은 내용을 Parquet로 copy했다. 이 구성이 있어서 07번과 10번이 lake-like 산출물을 재활용할 수 있다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json`
- 검증 신호:
  - `ingested 4 records` 출력 뒤 `.artifacts/log-basics.parquet`가 생긴다.
  - README가 DuckDB table과 Parquet 산출물을 공식 출력으로 문서화하고 있다.
- 핵심 코드 앵커: `00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py:58-78`
- 새로 배운 것: DuckDB + Parquet 조합은 로컬 학습에서도 security lake 사고방식을 체험하기에 충분하다. DB는 질의용, Parquet는 전달 가능한 산출물 역할을 한다.
- 다음: 적재만으로는 부족하니, 실제 집계와 기간 질의를 테스트에 넣어 ETL의 효용을 증명해야 했다.

## Phase 3. 집계 쿼리와 time range를 테스트로 잠갔다

이 구간에서는 `집계 쿼리와 time range를 테스트로 잠갔다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 적재 결과가 정말 queryable한지 확인한다.
- 변경 단위: `python/src/cloudtrail_log_basics/etl.py`의 summary 함수들, `python/tests/test_etl.py`
- 처음 가설: ETL이 제대로 됐다는 말은 파일이 생겼다는 뜻이 아니라, event name/actor/time range 질의가 의도한 결과를 돌려준다는 뜻이다.
- 실제 조치: `summarize_by_event_name`, `summarize_by_actor`, `within_time_range`를 추가해 실제 질의 경로를 만들고, 테스트는 4개의 이벤트가 어떤 이름과 기간으로 집계되는지 구체적으로 고정했다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests`
- 검증 신호:
  - pytest가 `1 passed in 0.13s`로 통과했다.
  - 테스트는 `CreateAccessKey`, `PutBucketAcl`, `flow:22`, `flow:443` 집계와 2건의 기간 내 이벤트를 정확히 요구했다.
- 핵심 코드 앵커: `00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py:18-35`
- 새로 배운 것: 정규화의 성공은 raw schema 보존이 아니라, 필요한 질문을 얼마나 짧은 query로 풀 수 있느냐로 판단하는 편이 좋다.
- 다음: 다음 프로젝트는 이 감각을 한 단계 밀어, 적재된 이벤트 위에서 탐지 쿼리를 직접 돌린다.

# 10 Development Timeline

이 문서는 `CloudTrail Log Basics`를 현재 fixture, ETL 코드, 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 로그를 저장하는 예제가 아니라, 이후 query와 detection이 가능한 입력 구조를 고정하는 단계인지 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `etl.py`, `test_etl.py`를 묶어서 읽었다.
- 이슈: 처음엔 CloudTrail만 정규화하면 된다고 생각했는데, 테스트를 보니 VPC Flow Logs까지 같은 `EventRecord`로 합쳐야 이후 집계 helper가 공통으로 동작했다.
- 판단: 이 프로젝트의 핵심은 로그 종류별 파서가 아니라, 서로 다른 원본을 `occurred_at`, `source`, `event_name`, `actor`, `resource_id`, `action_result`로 압축하는 공통 계약이었다.

CLI:

```bash
$ sed -n '1,120p' 00-aws-security-foundations/03-cloudtrail-log-basics/problem/README.md
$ sed -n '1,220p' 00-aws-security-foundations/03-cloudtrail-log-basics/python/src/cloudtrail_log_basics/etl.py
$ sed -n '1,200p' 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests/test_etl.py
```

이 시점의 핵심 코드는 CloudTrail과 VPC Flow Logs를 같은 dataclass로 모으는 부분이었다.

```python
@dataclass(slots=True)
class EventRecord:
    occurred_at: str
    source: str
    event_name: str
    actor: str
    resource_id: str
    action_result: str
```

처음엔 DuckDB 적재가 중심이라고 생각했지만, 나중에 보니 그보다 먼저 `EventRecord`를 얼마나 작고 공통적으로 정의하느냐가 중요했다. 이 구조가 정해져야 `summarize_by_event_name`, `summarize_by_actor`, `within_time_range`가 한 테이블에서 같이 동작한다.

### Session 2

- 진행: ETL CLI와 pytest를 다시 돌려 현재 README의 대표 출력과 집계 계약을 확인했다.
- 검증: CLI는 `ingested 4 records`를 출력했고, 테스트는 Parquet 생성과 event/actor/time-range 집계를 모두 통과했다.
- 판단: 처음 가설은 Parquet 생성만 확인하면 충분하다는 쪽이었지만, 테스트가 `within_time_range()`까지 고정하고 있어 적재와 조회를 분리해서 볼 수 없었다.
- 다음: 07번 `Security Lake Mini`는 여기서 만든 정규화 감각을 더 좁은 detection query로 바로 이어받는다.

CLI:

```bash
$ make venv
$ PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m cloudtrail_log_basics.etl 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/cloudtrail_events.json 00-aws-security-foundations/03-cloudtrail-log-basics/problem/data/vpc_flow_logs.json
$ PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

출력:

```text
ingested 4 records
1 passed in 0.41s
```

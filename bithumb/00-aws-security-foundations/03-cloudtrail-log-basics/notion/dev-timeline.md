# 03 CloudTrail Log Basics — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.
소스코드만으로는 알 수 없는 DuckDB 설치, Parquet 생성, fixture 설계 의도를 담고 있다.

---

## 1단계: 환경 준비

### 가상환경과 의존성

프로젝트 루트의 공용 가상환경을 사용한다. 이 과제에서 추가로 필요한 패키지는 `duckdb`다.

```bash
cd study2
make venv
```

`pyproject.toml`에 `duckdb>=1.3.2`가 포함되어 있으므로 `make venv`로 자동 설치된다.

### DuckDB 설치 확인

```bash
.venv/bin/python -c "import duckdb; print(duckdb.__version__)"
```

DuckDB는 별도 프로세스를 띄우지 않는다. Python 라이브러리로 임포트해서 사용한다.

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
03-cloudtrail-log-basics/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── log-normalization.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       ├── cloudtrail_events.json
│       └── vpc_flow_logs.json
└── python/
    ├── README.md
    ├── src/
    │   └── cloudtrail_log_basics/
    │       ├── __init__.py
    │       └── etl.py
    └── tests/
        └── test_etl.py
```

```bash
mkdir -p 00-aws-security-foundations/03-cloudtrail-log-basics/{docs/{concepts,references},problem/data,python/{src/cloudtrail_log_basics,tests}}
```

---

## 3단계: fixture 데이터 작성

### cloudtrail_events.json

실제 CloudTrail 로그와 동일한 구조의 fixture를 작성했다.
두 가지 이벤트를 포함:

1. **PutBucketAcl**: S3 버킷 ACL 변경 — 데이터 노출 위험이 있는 이벤트
2. **CreateAccessKey**: IAM 액세스 키 생성 — 계정 탈취 시 가장 먼저 발생하는 이벤트 중 하나

각 이벤트는 `eventTime`, `eventSource`, `eventName`, `userIdentity`, `requestParameters`를 포함한다.

### vpc_flow_logs.json

VPC Flow Logs 스타일 JSON fixture를 작성했다.
두 가지 플로우 레코드를 포함:

1. **443번 포트 ACCEPT**: 정상 HTTPS 트래픽
2. **22번 포트 ACCEPT**: SSH 트래픽 — security group 설정에 따라 주의 필요

각 레코드는 `timestamp`, `source_ip`, `destination_port`, `interface_id`, `action`을 포함한다.

---

## 4단계: 핵심 ETL 코드 작성

### etl.py 구현 순서

1. **EventRecord 데이터 클래스 정의**
   - 6개 공통 필드: `occurred_at`, `source`, `event_name`, `actor`, `resource_id`, `action_result`
   - 이 스키마가 두 종류의 로그를 하나로 통합하는 핵심

2. **normalize_cloudtrail_events() 함수**
   - `Records` 배열을 순회하며 EventRecord로 변환
   - `resource_id` 추출 시 `requestParameters`에서 `bucketName` → `userName` → `"unknown"` 순으로 fallback
   - `action_result`는 `"cloudtrail"`로 태그

3. **normalize_vpc_flow_logs() 함수**
   - 각 entry를 EventRecord로 변환
   - `event_name`을 `"flow:{destination_port}"` 형태로 생성
   - `actor`는 `source_ip`, `resource_id`는 `interface_id`

4. **ingest_records() 함수**
   - DuckDB 테이블 생성 (`event_records`)
   - `executemany`로 레코드 일괄 삽입
   - `COPY TO` 명령으로 Parquet 파일 생성

5. **요약 함수 3개**
   - `summarize_by_event_name()`: `GROUP BY event_name`
   - `summarize_by_actor()`: `GROUP BY actor`
   - `within_time_range()`: 시간 범위 필터링

---

## 5단계: 테스트 작성

### test_etl.py

하나의 통합 테스트로 전체 파이프라인을 검증:

1. fixture JSON 로드
2. 두 종류의 로그를 정규화
3. `tmp_path`에 DuckDB 파일과 Parquet 파일 생성
4. Parquet 파일 존재 확인
5. `summarize_by_event_name()` 결과 검증 — 4개 이벤트가 각각 1건씩
6. `summarize_by_actor()` 검증
7. `within_time_range()` 검증 — 특정 시간대에 2건

`tmp_path`는 pytest가 제공하는 임시 디렉토리로, 테스트 후 자동 정리된다.

---

## 6단계: 실행과 검증

### CLI로 ETL 실행

```bash
cd python
PYTHONPATH=src python -m cloudtrail_log_basics.etl ../problem/data/cloudtrail_events.json ../problem/data/vpc_flow_logs.json
```

출력:
```
ingested 4 records
```

생성되는 파일:
- `.artifacts/log-basics.duckdb` — DuckDB 데이터베이스 파일
- `.artifacts/log-basics.parquet` — Parquet 파일

### DuckDB로 직접 질의해 보기

```bash
.venv/bin/python -c "
import duckdb
conn = duckdb.connect('.artifacts/log-basics.duckdb')
print(conn.execute('SELECT event_name, COUNT(*) FROM event_records GROUP BY 1 ORDER BY 1').fetchall())
"
```

### Parquet 파일 확인

```bash
.venv/bin/python -c "
import duckdb
conn = duckdb.connect()
print(conn.execute(\"SELECT * FROM read_parquet('.artifacts/log-basics.parquet')\").fetchall())
"
```

### 테스트 실행

```bash
cd study2
PYTHONPATH=00-aws-security-foundations/03-cloudtrail-log-basics/python/src .venv/bin/python -m pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests
```

또는:

```bash
make test-unit
```

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| 핵심 의존성 | duckdb |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 |
| 외부 서비스 의존 | 없음 |
| 생성되는 아티팩트 | .duckdb 파일, .parquet 파일 |

---

## 주의사항

- `.artifacts/` 디렉토리는 자동 생성되지만, git에는 올리지 않는다.
- DuckDB 파일은 프로세스별로 잠금이 걸리므로, 동시에 두 프로세스가 같은 DB에 접근하면 에러가 발생한다.
- Parquet 파일은 한 번 쓰면 수정 불가(immutable)이므로, 재실행 시 덮어쓰기된다.
- fixture의 시간 값은 `2026-03-07T09:00:00Z` 형태이므로, 시간 범위 테스트에서 이 값을 기준으로 확인한다.

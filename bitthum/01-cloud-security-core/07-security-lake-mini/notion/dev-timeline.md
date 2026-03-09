# 07 Security Lake Mini — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.

---

## 1단계: 환경 준비

```bash
cd study2
make venv
```

이 과제에서 사용하는 패키지: `duckdb`, `typer`. 둘 다 `pyproject.toml`에 포함.

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
07-security-lake-mini/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── lake-thinking.md
│   └── references/
│       └── README.md
├── problem/
│   ├── README.md
│   └── data/
│       └── cloudtrail_suspicious.json
└── python/
    ├── README.md
    ├── src/
    │   └── security_lake_mini/
    │       ├── __init__.py
    │       ├── cli.py
    │       └── lake.py
    └── tests/
        └── test_lake.py
```

```bash
mkdir -p 01-cloud-security-core/07-security-lake-mini/{docs/{concepts,references},problem/data,python/{src/security_lake_mini,tests}}
```

---

## 3단계: fixture 데이터 작성

### cloudtrail_suspicious.json

다섯 가지 의심스러운 이벤트를 포함하는 CloudTrail fixture:

1. **CreateAccessKey** — IAM 키 생성
2. **PutBucketAcl** — S3 ACL 변경
3. **AuthorizeSecurityGroupIngress** — Security Group 인바운드 규칙 추가
4. **DeleteTrail** — CloudTrail 삭제 (가장 위험)
5. **ConsoleLogin** (root) — root 계정 콘솔 로그인

각 이벤트는 CloudTrail 표준 구조(`eventTime`, `eventSource`, `eventName`, `userIdentity`)를 따른다.
`userIdentity.arn`의 마지막 세그먼트가 `:root`인 경우 LAKE-005로 탐지된다.

---

## 4단계: 핵심 엔진 구현

### lake.py 작성

구현 순서:

1. **Alert 데이터 클래스 정의**
   - `control_id`, `title`, `event_name`, `actor`, `occurred_at`
   - Finding과 다른 구조: 행위 기반이므로 `event_name`과 `actor`가 핵심

2. **_normalize() 내부 함수**
   - CloudTrail Records를 `(occurred_at, source, event_name, actor)` 튜플로 변환
   - `userIdentity`에서 `arn` 추출, 없으면 `"unknown"`

3. **ingest_cloudtrail() 함수**
   - JSON 로드 → 정규화 → DuckDB 테이블 생성/초기화 → 데이터 삽입 → Parquet 내보내기
   - `DELETE FROM lake_events`로 기존 데이터 초기화 (멱등성 보장)

4. **run_detection_queries() 함수**
   - 하나의 SQL 쿼리로 다섯 가지 이벤트 탐지
   - `CASE WHEN`으로 control_id 할당
   - `WHERE event_name IN (...)` 필터
   - `LAKE-005`는 추가 조건: `actor LIKE '%:root'`
   - 결과를 Alert 리스트로 반환

---

## 5단계: CLI 작성

### cli.py

세 개의 인자: CloudTrail JSON 경로, DuckDB 경로, Parquet 경로.

```bash
touch python/src/security_lake_mini/__init__.py
```

---

## 6단계: 테스트 작성

### test_lake.py

하나의 통합 테스트:

1. fixture CloudTrail JSON 로드
2. `tmp_path`에 DuckDB + Parquet 생성
3. `ingest_cloudtrail` 실행
4. Parquet 파일 존재 확인
5. `run_detection_queries` 실행
6. 결과 alert의 `control_id` 순서 검증: `["LAKE-001", "LAKE-002", "LAKE-003", "LAKE-004", "LAKE-005"]`

모든 detection rule이 정확히 한 번씩 발동하는지 확인한다.

---

## 7단계: 실행과 검증

### CLI 실행

```bash
cd python
PYTHONPATH=src python -m security_lake_mini.cli ../problem/data/cloudtrail_suspicious.json .artifacts/lake.duckdb .artifacts/events.parquet
```

### 적재 확인

```bash
cd study2
.venv/bin/python -c "
import duckdb
conn = duckdb.connect('.artifacts/lake.duckdb')
print(conn.execute('SELECT * FROM lake_events ORDER BY occurred_at').fetchall())
"
```

### detection query 직접 실행

```bash
.venv/bin/python -c "
from pathlib import Path
from security_lake_mini.lake import ingest_cloudtrail, run_detection_queries
import sys; sys.path.insert(0, '01-cloud-security-core/07-security-lake-mini/python/src')

ingest_cloudtrail(
    Path('01-cloud-security-core/07-security-lake-mini/problem/data/cloudtrail_suspicious.json'),
    Path('.artifacts/lake.duckdb'),
    Path('.artifacts/lake.parquet')
)
for alert in run_detection_queries(Path('.artifacts/lake.duckdb')):
    print(f'{alert.control_id}: {alert.event_name} by {alert.actor}')
"
```

### 테스트 실행

```bash
cd study2
PYTHONPATH=01-cloud-security-core/07-security-lake-mini/python/src .venv/bin/python -m pytest 01-cloud-security-core/07-security-lake-mini/python/tests
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
| 핵심 의존성 | duckdb, typer |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 |
| 외부 서비스 의존 | 없음 |
| 생성되는 아티팩트 | .duckdb 파일, .parquet 파일 |
| 테스트 카테고리 | Unit |

---

## 주의사항

- `ingest_cloudtrail`은 기존 데이터를 `DELETE`한 뒤 다시 삽입한다.
  같은 DB 파일에 여러 번 실행해도 데이터가 중복되지 않는다.
- DuckDB 파일 잠금에 주의. 한 프로세스가 잡고 있으면 다른 프로세스가 접근할 수 없다.
- fixture의 모든 이벤트는 동일한 시간대(2026-03-07)에 몰려 있다.
  실제 운영에서는 시간 분포가 넓을 수 있다.

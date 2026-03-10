# 10 Cloud Security Control Plane — 개발 타임라인

이 문서는 캡스톤 프로젝트를 처음부터 재현할 때 필요한 모든 단계를 순서대로 기록한다.

---

## 1단계: 환경 준비

### Python 환경

```bash
cd study2
make venv
```

### Docker 설치 확인

```bash
docker --version
docker compose version
```

Docker Desktop이 실행 중이어야 한다.

### PostgreSQL 컨테이너 기동

```bash
make capstone-up
```

내부적으로 실행되는 명령:
```bash
docker compose up -d
```

`docker-compose.yml`의 내용:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: study2-control-plane-postgres
    environment:
      POSTGRES_USER: study2
      POSTGRES_PASSWORD: study2
      POSTGRES_DB: control_plane
    ports:
      - "54340:5432"
```

### 접속 확인

```bash
docker exec -it study2-control-plane-postgres psql -U study2 -d control_plane -c "SELECT 1"
```

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
10-cloud-security-control-plane/
├── README.md
├── docs/
│   ├── README.md
│   ├── demo-walkthrough.md
│   ├── concepts/
│   ├── demo-assets/
│   └── references/
├── problem/
│   ├── README.md
│   └── data/
│       ├── sample_plan.json
│       ├── sample_cloudtrail.ndjson
│       └── sample_k8s.yaml
└── python/
    ├── README.md
    ├── src/
    │   └── control_plane/
    │       ├── __init__.py
    │       ├── app.py
    │       ├── cli.py
    │       ├── db.py
    │       ├── demo_capture.py
    │       ├── metrics.py
    │       ├── remediation.py
    │       ├── reporting.py
    │       ├── scanners.py
    │       ├── schemas.py
    │       └── workers.py
    └── tests/
        └── test_app.py
```

```bash
mkdir -p 02-capstone/10-cloud-security-control-plane/{docs/{concepts,references,demo-assets},problem/data,python/{src/control_plane,tests}}
```

---

## 3단계: 데이터베이스 모델 (db.py)

가장 먼저 작성하는 파일. 나머지 모듈이 전부 이 모델에 의존한다.

### 핵심 테이블

| 테이블 | 역할 |
|--------|------|
| ScanRequest | 스캔 요청 (type, status, created_at) |
| Finding | 탐지 결과 (control_id, severity, resource, detail) |
| Exception | 예외 (finding 연결, reason, status, expires) |
| Evidence | 증거 (exception 연결, type, content) |
| AuditEvent | 감사 이벤트 (exception 연결, event_type, actor) |

### DB 연결 설정

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://study2:study2@localhost:54340/control_plane"
)
```

### 테이블 자동 생성

```python
Base.metadata.create_all(bind=engine)
```

이 접근은 개발용이다. 프로덕션에서는 Alembic 마이그레이션을 사용한다.

---

## 4단계: Pydantic 스키마 (schemas.py)

API 요청/응답 검증용 Pydantic v2 모델:

- `ScanRequestCreate`: type, path 등
- `FindingResponse`: control_id, severity 등
- `ExceptionCreate`: finding_id, reason, expires
- `ReportRequest`: format, filters

---

## 5단계: 스캐너 통합 (scanners.py)

이전 과제들의 핵심 로직을 하나의 모듈로:

```python
def scan_terraform_plan(plan_path: str) -> list[dict]:
    """과제 02, 04의 Terraform plan 분석"""

def scan_iam_policies(policy_path: str) -> list[dict]:
    """과제 01, 04의 IAM 정책 평가"""

def scan_cloudtrail_logs(log_path: str) -> list[dict]:
    """과제 03의 CloudTrail ETL + DuckDB 분석"""

def scan_k8s_manifest(manifest_path: str) -> list[dict]:
    """과제 08의 K8s YAML 검사"""
```

각 함수는 동일한 finding 포맷을 반환한다.
이전 과제의 다양한 finding 구조를 여기서 정규화한다.

---

## 6단계: Worker 구현 (workers.py)

### 스캔 Worker

```python
def run_scan_worker(scan_request_id: str, db_session):
    request = db_session.get(ScanRequest, scan_request_id)
    request.status = "running"

    scanner = SCANNER_MAP[request.scan_type]
    findings = scanner(request.target_path)

    for f in findings:
        db_session.add(Finding(**f, scan_request_id=scan_request_id))

    request.status = "completed"
    db_session.commit()
```

### Remediation Worker

과제 06의 dry-run/execute 패턴을 재사용.
finding에 대한 수정 작업을 제안하거나 실행한다.

---

## 7단계: FastAPI 애플리케이션 (app.py)

### 엔드포인트 목록

| 메서드 | 경로 | 기능 |
|--------|------|------|
| POST | `/scans` | 스캔 요청 생성 |
| GET | `/scans/{id}` | 스캔 상태 조회 |
| GET | `/findings` | Finding 목록 조회 |
| POST | `/exceptions` | 예외 생성 |
| POST | `/exceptions/{id}/approve` | 예외 승인 |
| POST | `/exceptions/{id}/evidence` | 증거 첨부 |
| POST | `/reports` | 마크다운 리포트 생성 |

### 서버 실행

```bash
cd python
DATABASE_URL=postgresql+psycopg://study2:study2@localhost:54340/control_plane \
  PYTHONPATH=src uvicorn control_plane.app:app --port 8000
```

---

## 8단계: CLI (cli.py)

Typer 기반. API 서버 없이 DB 직접 접근:

```bash
PYTHONPATH=src python -m control_plane.cli findings
PYTHONPATH=src python -m control_plane.cli scan --type terraform --path ../problem/data/sample_plan.json
PYTHONPATH=src python -m control_plane.cli report
```

---

## 9단계: 리포트 & 메트릭 (reporting.py, metrics.py)

### 리포트

Finding과 Exception을 마크다운 테이블로 렌더링.
severity별 요약, scanner별 분류, 예외 처리 현황 포함.

### 메트릭

Finding 데이터에서 수치 추출:
- Critical/High/Medium/Low 분포
- Scanner별 finding 수
- 시간대별 추이

---

## 10단계: 데모 캡처 (demo_capture.py)

전체 흐름을 자동으로 실행하는 스크립트:

```bash
make demo-capstone
```

내부적으로:
```bash
docker compose up -d
cd python
PYTHONPATH=src python -m control_plane.demo_capture
```

### 데모 흐름

1. Terraform plan 스캔 요청 → Worker 실행 → findings 수집
2. CloudTrail 로그 ingestion
3. K8s manifest ingestion
4. 예외 생성 → 증거 첨부 → 승인
5. Remediation dry-run
6. 마크다운 리포트 생성
7. 결과를 `docs/demo-assets/`에 저장

---

## 11단계: 테스트

### 통합 테스트 (PostgreSQL 필요)

```bash
make test-capstone
```

### 가벼운 로컬 테스트 (SQLite)

```bash
DATABASE_URL=sqlite:///test_control_plane.db \
  PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src \
  .venv/bin/python -m pytest 02-capstone/10-cloud-security-control-plane/python/tests -v
```

### 전체 테스트 (모든 과제)

```bash
make test-all
```

---

## 12단계: 정리

### PostgreSQL 중지

```bash
make capstone-down
```

내부:
```bash
docker compose down
```

### 데이터 초기화가 필요한 경우

```bash
docker compose down -v
docker compose up -d
```

`-v` 플래그가 볼륨을 삭제하므로 DB 데이터가 초기화된다.

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| 핵심 의존성 | FastAPI, SQLAlchemy, psycopg, Pydantic, Typer, DuckDB, PyYAML, uvicorn |
| 데이터베이스 | PostgreSQL 16-alpine (Docker) 또는 SQLite (폴백) |
| 컨테이너 | Docker Compose |
| PostgreSQL 포트 | 54340 (호스트) → 5432 (컨테이너) |
| DB 사용자/비밀번호 | study2 / study2 |
| DB 이름 | control_plane |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 |
| 테스트 카테고리 | Integration |

---

## 주의사항

- PostgreSQL 컨테이너가 실행 중이어야 기본 설정으로 테스트/데모가 동작한다.
  `docker ps`로 `study2-control-plane-postgres`가 보이는지 확인.
- 포트 54340이 이미 사용 중이면 `docker-compose.yml`의 ports를 변경해야 한다.
- `create_all`은 기존 테이블이 있으면 건너뛴다.
  스키마를 변경했으면 `docker compose down -v && docker compose up -d`로 초기화.
- SQLite 폴백에서는 일부 PostgreSQL 전용 기능이 동작하지 않을 수 있다.
  기본 CRUD와 단위 테스트는 SQLite에서도 통과한다.

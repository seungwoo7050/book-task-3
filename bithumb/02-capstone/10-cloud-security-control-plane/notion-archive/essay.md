# 9개의 과제가 하나의 서비스가 될 때

## 이 과제의 존재 이유

과제 01부터 09까지, 각각은 독립적인 Python 모듈이었다.
IAM 정책을 평가하고, Terraform을 검증하고, CloudTrail 로그를 분석하고,
CSPM 규칙을 돌리고, 컨테이너 manifest를 검사하고, 예외를 관리했다.
전부 CLI로 실행하고 JSON을 표준출력에 찍는 방식이었다.

하지만 실무의 CSPM 제품은 이렇게 동작하지 않는다.
스캔 요청이 API로 들어오고, 결과가 데이터베이스에 저장되고,
대시보드에서 찾아보고, 리포트로 내보내는 흐름이 있다.

이 캡스톤은 그 흐름을 최소 단위로 구현한다.
FastAPI로 API를 만들고, SQLAlchemy로 DB에 저장하고,
Worker가 비동기로 스캔을 실행하고, 마크다운 리포트를 생성한다.
9개 과제의 핵심 로직을 이 하나의 서비스 안에서 재사용한다.

## 아키텍처

### 네 개의 레이어

**1. API 레이어 (app.py)**
- FastAPI 애플리케이션
- 엔드포인트: scan request 생성, finding 조회, 예외 관리, 리포트 생성
- Pydantic 스키마로 요청/응답 검증
- `@app.on_event("startup")`에서 DB 테이블 생성

**2. 데이터 레이어 (db.py)**
- SQLAlchemy ORM
- 테이블: ScanRequest, Finding, Exception, Evidence, AuditEvent
- `DATABASE_URL` 환경 변수로 PostgreSQL/SQLite 전환
- 기본값은 PostgreSQL (`postgresql+psycopg://...`)
- SQLite 폴백: `sqlite:///control_plane.db`

**3. Worker 레이어 (workers.py)**
- `run_scan_worker`: scan request를 받아 적절한 scanner를 실행하고 finding을 DB에 저장
- `run_remediation_worker`: 지정된 finding에 대해 dry-run 또는 실제 remediation 실행
- 동기 실행이지만, 실제 백그라운드 큐(Celery, SQS 등)로 교체 가능한 구조

**4. Scanner 레이어 (scanners.py)**
- 과제별 scanner를 통합:
  - `scan_terraform_plan()` — Terraform plan JSON 분석
  - `scan_iam_policies()` — IAM 정책 과다 권한 탐지
  - `scan_cloudtrail_logs()` — CloudTrail NDJSON 파싱 + DuckDB 분석
  - `scan_k8s_manifest()` — K8s YAML 보안 검사

### 왜 Worker를 분리했나

API 요청 핸들러 안에서 스캔을 직접 실행하면,
대용량 CloudTrail 로그를 분석할 때 HTTP 타임아웃이 발생할 수 있다.

Worker를 분리하면:
1. API는 scan request를 DB에 기록하고 즉시 응답 (202 Accepted 패턴)
2. Worker는 request를 polling해서 비동기로 처리
3. 상태 업데이트: `pending → running → completed`

이 구현에서는 `threading.Thread`로 Worker를 실행하지만,
프로덕션에서는 Celery나 AWS SQS를 사용한다.

## 9개 과제 통합 지점

| 과제 | Control Plane에서의 역할 |
|------|--------------------------|
| 01 IAM primitives | `scan_iam_policies` — 정책 평가 로직 재사용 |
| 02 Terraform Lab | `scan_terraform_plan` — plan JSON 분석 재사용 |
| 03 CloudTrail ETL | `scan_cloudtrail_logs` — DuckDB ETL 파이프라인 재사용 |
| 04 IAM Analyzer | IAM 스캐너의 위험도 분류 로직 |
| 05 CSPM Rule Engine | Finding 구조와 severity 체계가 동일 |
| 06 Remediation Runner | `run_remediation_worker` — dry-run/execute 패턴 |
| 07 Security Lake | DuckDB 기반 분석 쿼리 패턴 |
| 08 Container Guardrails | `scan_k8s_manifest` — K8s YAML 검사 재사용 |
| 09 Exception Manager | 예외 생성/승인/증거 첨부 흐름 — DB 위에서 영속화 |

과제 09에서 in-memory였던 ExceptionManager가
여기서 SQLAlchemy 테이블로 교체되었다.
`create → approve → is_suppressed` 흐름은 동일하지만,
데이터가 PostgreSQL에 영속화된다.

## DB 선택: PostgreSQL과 SQLite 폴백

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://study2:study2@localhost:54340/control_plane"
)
```

기본값은 PostgreSQL이다.
Docker Compose로 PostgreSQL 16-alpine을 띄우면 바로 연결된다.

CI 환경이나 빠른 로컬 테스트에서는 SQLite를 사용할 수도 있다:
```bash
DATABASE_URL=sqlite:///control_plane.db make test-capstone
```

왜 psycopg(v3)인가:
- psycopg2는 C 확장이 필요해서 설치가 까다롭다
- psycopg(v3)는 pure-Python 모드를 지원하고, async도 가능하다
- SQLAlchemy 2.0과의 호환성이 더 좋다

## 데모 캡처 시스템

`demo_capture.py`는 데모 시연용 스크립트다.
API를 호출해서 전체 흐름을 자동으로 수행하고,
각 단계의 결과를 파일로 저장한다.

흐름:
1. 스캔 요청 생성 (Terraform plan)
2. Worker가 스캔 실행
3. Finding 목록 조회
4. CloudTrail 로그 ingestion
5. K8s manifest ingestion
6. 예외 생성 및 승인
7. Remediation dry-run
8. 마크다운 리포트 생성

이 흐름이 `make demo-capstone` 한 줄로 실행된다.

## CLI (cli.py)

Typer 기반 CLI로, DB를 직접 조회하는 관리 도구다:

```bash
python -m control_plane.cli findings
python -m control_plane.cli report
python -m control_plane.cli scan --type terraform --path plan.json
```

API 서버 없이도 핵심 기능을 사용할 수 있다.

## 메트릭스 (metrics.py)

Finding 데이터에서 통계를 추출한다:
- severity 별 finding 수
- scanner 별 finding 수  
- 시간대별 finding 추이

대시보드 없이도 보안 상태를 수치로 파악할 수 있다.

## 마크다운 리포트 (reporting.py)

Finding과 Exception 데이터를 읽어서 마크다운 문서를 생성한다.
표(table), 요약 통계, severity 분포가 포함된다.

이 리포트는 GitHub 이슈나 Confluence 페이지에 바로 붙여넣을 수 있는 형식이다.

## 실제로 만들어 본 뒤에 체감한 것

가장 어려웠던 건 "9개 과제의 인터페이스를 통일하는 것"이었다.
각 과제의 finding은 비슷하지만 필드 이름이 미묘하게 달랐다.
Control Plane에서는 모든 finding이 동일한 SQLAlchemy 모델에 매핑되어야 하므로,
scanner 레이어에서 정규화(normalization)하는 작업이 필요했다.

Docker Compose로 PostgreSQL을 띄우고, SQLAlchemy의 `create_all`로 테이블을 자동 생성하는 패턴은
첫 사용자가 추가 SQL 스크립트 없이 바로 시작할 수 있게 해준다.
하지만 스키마 변경이 생기면 Alembic 같은 마이그레이션 도구가 필요해진다.
v1에서는 "테이블을 자동 생성하고, 변경이 필요하면 DB를 다시 만든다"는 단순한 전략을 택했다.

## 이 과제의 위치

이 프로젝트는 트랙 전체의 최종 결과물이다.
Phase 0 (AWS 기초 3개) → Phase 1 (핵심 보안 도구 6개) → Phase 2 (통합) 순으로,
마지막에 모든 것이 하나의 서비스로 합쳐진다.

포트폴리오에서 이 프로젝트를 설명할 때:
- "9개 독립 모듈을 하나의 REST API 서비스로 통합했습니다"
- "FastAPI + SQLAlchemy + PostgreSQL 스택에서 스캔 → 탐지 → 예외 → 리포트 파이프라인을 구현했습니다"
- "Docker Compose로 로컬 환경을 one-command로 재현할 수 있게 만들었습니다"

## 한계와 v1 범위

- 인증/인가 없음 (FastAPI의 OAuth2/JWT 미적용)
- Worker가 threading 기반 — 프로덕션에서는 Celery/SQS 권장
- 마이그레이션 도구(Alembic) 미도입 — 스키마 변경 시 DB 재생성 필요
- 모니터링/알림 없음 — Prometheus/Grafana 연동 미구현
- 멀티테넌트 미지원
- 실제 AWS API 호출 없음 — 모든 데이터가 로컬 fixture

# 공통 기반에서 세 캡스톤으로 — 제출 경로 가이드

세 개의 캡스톤으로 수렴하는 학습 경로와 각 분기별 완료 기준을 정의한다.  
제출 최종 판정은 [submission-readiness-rubric.md](submission-readiness-rubric.md)를 사용한다.

---

## 캡스톤 세 분기

| 분기 | 경로 | 핵심 도메인 |
|------|------|------------|
| **A** | `infobank/chat-qa-ops` | Python 백엔드 · LLM 파이프라인 · DevOps |
| **B** | `bithumb/02-capstone/10-cloud-security-control-plane` | 클라우드 보안 · IaC · 컨트롤 플레인 |
| **C** | `cpp-server/study/arenaserv` | C++ 서버 · 게임 네트워크 · 성능 |

---

## 1. 공통 선행 학습 순서

세 분기 모두 아래 공통 기반을 먼저 완료한다. 순서는 의존 관계 기준이다.

### 1-1. 언어

| 순서 | 항목 | 안내서 |
|------|------|--------|
| 1 | Python 기초 | [guides/language/python.md](../language/python.md) |
| 2 | C++ 기초 | [guides/language/cpp.md](../language/cpp.md) |
| 3 | Go 기초 (선택) | [guides/language/go.md](../language/go.md) |

> 분기 A·B는 Python 우선, 분기 C는 C++ 우선.

### 1-2. 백엔드

| 순서 | 항목 | 안내서 |
|------|------|--------|
| 1 | HTTP 서버 기본 구조 | [guides/backend/fastapi.md](../backend/fastapi.md) 또는 [nodejs.md](../backend/nodejs.md) |
| 2 | 비동기 작업 패턴 | [guides/backend/celery.md](../backend/celery.md) |
| 3 | gRPC (분기 B·C 필요) | [guides/backend/grpc.md](../backend/grpc.md) |

### 1-3. 데이터베이스

| 순서 | 항목 | 안내서 |
|------|------|--------|
| 1 | SQL 기본 | [guides/database/sql.md](../database/sql.md) |
| 2 | Redis | [guides/database/redis.md](../database/redis.md) |

### 1-4. DevOps (모든 분기 공통)

| 순서 | 항목 | 안내서 |
|------|------|--------|
| 1 | Docker 이미지 빌드 | [guides/devops/docker.md](../devops/docker.md) |
| 2 | Docker Compose 로컬 환경 | [guides/devops/docker-compose.md](../devops/docker-compose.md) |
| 3 | GitHub Actions CI | [guides/devops/github-actions.md](../devops/github-actions.md) |
| 4 | 관측성·신뢰성 기본 | [guides/devops/observability-reliability.md](../devops/observability-reliability.md) |
| 5 | 장애 주입 훈련 | [guides/devops/failure-injection.md](../devops/failure-injection.md) |
| 6 | 로드 테스트 | [guides/testing/load-testing.md](../testing/load-testing.md) |

---

## 2. 분기별 추가 선행 조건

공통 기반 완료 후 각 분기 진입 전에 아래를 추가로 확인한다.

### 분기 A — `infobank/chat-qa-ops`

```
추가 선행 조건
├── LLM API 기본 사용 경험 (OpenAI / Anthropic SDK)
├── 벡터 DB 개념 이해 (RAG 파이프라인)
├── Celery + Redis 비동기 큐 실습 완료
└── Docker Compose 다중 서비스 구성 경험
```

### 분기 B — `bithumb/02-capstone/10-cloud-security-control-plane`

```
추가 선행 조건
├── Terraform 기본 실습 완료
│   └── guides/devops/terraform.md
├── AWS IAM / VPC 개념 이해
├── 클라우드 보안 원칙 (최소 권한, 감사 로깅)
└── Python boto3 SDK 기본 사용
```

### 분기 C — `cpp-server/study/arenaserv`

```
추가 선행 조건
├── C++ 소켓 프로그래밍 기초
├── CMake 빌드 시스템 구성 경험
│   └── guides/tool/cmake.md
├── 포인터, RAII, std::thread 이해
└── 간단한 클라이언트-서버 에코 서버 구현 완료
```

---

## 3. 분기별 Completion Gate

"submit-ready" 상태는 다음 조건을 **모두** 충족한 상태로 정의한다.

### 분기 A — chat-qa-ops

```
[ ] 핵심 기능 동작
    ├── 질문 입력 → LLM 응답 반환 (end-to-end)
    ├── 비동기 작업 큐 처리 (Celery or 동등 수단)
    └── 응답 캐시 또는 세션 관리 동작

[ ] 재현 가능성
    ├── docker compose up 한 줄로 전체 기동
    └── .env.example 또는 환경 변수 문서 존재

[ ] 테스트 증거
    ├── pytest 단위 테스트 통과
    └── load-testing.md baseline 단계 결과 첨부

[ ] 운영 증거
    ├── /health 엔드포인트 존재
    ├── 장애 주입 시나리오 1개 이상 실행 및 보고서
    └── Evidence Package (변경 전후 메트릭)

[ ] 문서
    ├── README에 빌드/실행/테스트 명령 포함
    └── 아키텍처 다이어그램 (텍스트 도표 가능)
```

### 분기 B — cloud-security-control-plane

```
[ ] 핵심 기능 동작
    ├── 보안 정책 평가 또는 컨트롤 플레인 API 응답
    ├── IaC (Terraform) plan 오류 없음
    └── 감사 로그 생성 확인

[ ] 재현 가능성
    ├── Terraform init → plan → apply 가이드 문서화
    └── 로컬 실행 또는 LocalStack 대안 제공

[ ] 테스트 증거
    ├── 단위 테스트 또는 정책 검증 스크립트 통과
    └── 침투 시나리오 1개 이상 실행 결과

[ ] 운영 증거
    ├── 감사 로그 샘플 첨부
    ├── 장애 시나리오 (의존 서비스 단절) 보고서
    └── Evidence Package

[ ] 문서
    ├── 보안 아키텍처 다이어그램
    ├── 위협 모델 요약 (1페이지)
    └── 런북: 접근 거부 발생 시 조사 절차
```

### 분기 C — arenaserv

```
[ ] 핵심 기능 동작
    ├── 다중 클라이언트 동시 연결 처리
    ├── 기본 게임 루프 또는 세션 관리 동작
    └── 정상 종료 (SIGTERM) 처리

[ ] 재현 가능성
    ├── cmake --build 또는 make 한 줄로 빌드
    └── 클라이언트 테스트 하네스 실행 방법 문서화

[ ] 테스트 증거
    ├── 단위 테스트 (Google Test 또는 동등 수단) 통과
    └── load-testing.md C++ 하네스 기반 결과 첨부

[ ] 운영 증거
    ├── 리소스 압박 시나리오 실행 결과
    ├── valgrind / AddressSanitizer 실행 리포트
    └── Evidence Package (p99 지연시간, 최대 동시 연결 수)

[ ] 문서
    ├── 서버 아키텍처 다이어그램
    ├── 메모리 관리 사양 요약
    └── 알려진 한계 (Known Limitations) 섹션
```

---

## 4. 공통 산출물과 분기별 필수 증거

### 4.1 모든 분기 공통 산출물

| 산출물 | 형식 | 위치 |
|--------|------|------|
| 아키텍처 다이어그램 | Markdown 텍스트 도표 또는 이미지 | `docs/` |
| 로드 테스트 결과 | 텍스트 보고서 | `docs/` 또는 README 삽입 |
| 인시던트 훈련 보고서 | Markdown | `docs/` |
| Evidence Package | README 내 섹션 | README.md |
| 빌드·테스트 명령 | README 코드블록 | README.md |

### 4.2 분기별 추가 필수 증거

**분기 A**

```
+ pytest 결과 출력 (--tb=short)
+ Celery 워커 로그 샘플 (정상 처리)
+ LLM API 응답 샘플 (민감 정보 마스킹 후)
```

**분기 B**

```
+ Terraform plan 출력 (또는 LocalStack apply 결과)
+ 감사 로그 샘플 (접근 거부 포함)
+ 위협 모델 요약 (1페이지)
```

**분기 C**

```
+ AddressSanitizer 또는 valgrind 실행 결과 (메모리 에러 없음)
+ 동시 연결 수 vs 지연시간 그래프 또는 표
+ 서버 종료 처리 로그 샘플
```

---

## 관련 문서

- [submission-readiness-rubric.md](submission-readiness-rubric.md) — 점수 기반 제출 판정 기준
- [observability-reliability.md](../devops/observability-reliability.md) — Evidence Package 포맷
- [load-testing.md](../testing/load-testing.md) — 테스트 단계별 실행 방법
- [failure-injection.md](../devops/failure-injection.md) — 인시던트 훈련 시나리오

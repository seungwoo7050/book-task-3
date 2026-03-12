# Curriculum Audit

## Goal

이 저장소의 직접 목표는 완전 초보가 Go 백엔드 주니어 후반 수준까지
올라가는 것이다. 미드 레벨은 이 커리큘럼의 직접 목표가 아니다.

## Legacy Strengths

- `net/http` 기반 API 설계
- Go 동시성 패턴과 레이트 리밋
- gRPC, commit log, outbox, transaction retry
- Docker, Helm, ArgoCD, capstone 통합 과제

## Legacy Gaps

- Go 문법과 타입 시스템 기초
- SQL 및 데이터 모델링의 입문형 과제
- HTTP/REST 기본기와 상태 코드 해석
- 테스트 설계와 디버깅 입문
- 인증/인가, 세션, JWT
- cache, migration, observability

## Study Decisions

- `00-go-fundamentals`를 새로 추가한다.
- `01-backend-core`에 SQL, HTTP, auth, cache/observability 브리지 과제를 추가한다.
- 기존 `concurrency-patterns`와 `rate-limiter`는 뒤로 이동한다.
- `distributed-log`는 `distributed-log-core`로 이름을 바꿔 실제 구현 범위에 맞춘다.
- `gitops-deploy`는 `solution/infra` 구조를 사용한다.
- `05-portfolio-projects`는 학습 순서를 유지하면서 채용용 대표작을 따로 두는 선택 트랙이다.

## Status Model

- `planned`: 구조만 있고 구현은 아직 없음
- `in-progress`: 구현 중이며 검증 기준이 아직 남아 있음
- `partial`: 일부 구현은 있으나 계획한 범위를 다 충족하지 못함
- `verified`: 문서에 적힌 핵심 build/test/run 명령이 실제로 통과함
- `archived`: 더 이상 본선 과제로 유지하지 않음

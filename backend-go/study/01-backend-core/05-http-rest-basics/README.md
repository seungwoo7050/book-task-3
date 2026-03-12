# 05 HTTP REST Basics

## 한 줄 요약

작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다.

## 이 프로젝트가 푸는 문제

- HTTP method와 상태 코드를 단순 암기가 아니라 직접 선택해야 한다.
- JSON request/response와 validation 흐름을 손으로 구현해야 한다.
- pagination과 idempotency key의 기본 의미를 API 문맥에서 익혀야 한다.

## 내가 만든 답

- `GET /v1/healthcheck`, `POST /v1/tasks`, 조회 API를 포함한 작은 JSON API를 `solution/go`에 구현했다.
- validation과 pagination을 handler 계층에서 직접 다루고, `Idempotency-Key` 헤더 의미를 최소 범위로 반영했다.
- 영속 저장소와 auth를 섞지 않고 HTTP 기초만 분리했다.

## 핵심 설계 선택

- 저장소 복잡도를 제거해 상태 코드와 요청 검증에 집중하도록 했다.
- idempotency는 완성형 분산 설계가 아니라 “왜 필요한가”를 보여 주는 최소 형태로 제한했다.

## 검증

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- 영속 저장소
- 인증/인가

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 브리지 과제

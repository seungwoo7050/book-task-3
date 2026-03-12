# 11 Rate Limiter

## 한 줄 요약

Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다.

## 이 프로젝트가 푸는 문제

- Token Bucket 알고리즘을 직접 구현해야 한다.
- per-client 분리와 stale client cleanup을 함께 처리해야 한다.
- HTTP middleware로 `429 Too Many Requests`와 `Retry-After`를 반환해야 한다.

## 내가 만든 답

- token bucket limiter와 per-client limiter를 `solution/go`에 구현했다.
- cleanup goroutine과 middleware integration을 같이 넣어 실제 서버 보호 흐름을 보여 준다.
- 분산 limiter 대신 단일 프로세스 동시성 안전성에 집중했다.

## 핵심 설계 선택

- rate limiter 자체와 HTTP middleware를 분리해 알고리즘과 네트워크 표면을 따로 읽게 했다.
- distributed limiter를 제외해 단일 프로세스 제어 흐름과 동기화 문제를 먼저 익히게 했다.

## 검증

- `cd solution/go && go test ./... -bench=.`
- `make -C problem test`
- `make -C problem bench`

## 제외 범위

- Redis-backed distributed limiter
- multi-node coordination

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/01-foundation/03-rate-limiter (`legacy/01-foundation/03-rate-limiter/README.md`, public repo에는 미포함)

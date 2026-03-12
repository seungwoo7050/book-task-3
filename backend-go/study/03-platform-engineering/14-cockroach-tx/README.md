# 14 Cockroach TX

## 한 줄 요약

idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다.

## 이 프로젝트가 푸는 문제

- 중복 요청, 동시 요청, CockroachDB retry를 한 purchase 흐름에서 다뤄야 한다.
- optimistic locking과 idempotency key를 같은 서비스 계층에서 구현해야 한다.
- SQLSTATE `40001` 재시도 helper를 제공해야 한다.

## 내가 만든 답

- repository, service, retry helper, HTTP purchase handler를 `solution/go`에 구현했다.
- balance version conflict와 idempotency cached response를 서비스 경계에서 구분한다.
- problem/Makefile과 runtime repro를 분리해 로컬 검증 진입점을 명확히 했다.

## 핵심 설계 선택

- DB가 요구하는 retry와 애플리케이션이 요구하는 idempotency를 한 흐름에서 분리해 보여 준다.
- HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.

## 검증

- `make -C problem build`
- `make -C problem test`
- `cd solution/go && make repro`

## 제외 범위

- 분산 트레이싱
- 멀티 리전 운영

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/03-platform-engineering/06-cockroach-tx (`legacy/03-platform-engineering/06-cockroach-tx/README.md`, public repo에는 미포함)

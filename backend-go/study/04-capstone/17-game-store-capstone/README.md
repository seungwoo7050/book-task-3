# 17 Game Store Capstone

## 한 줄 요약

거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다.

## 이 프로젝트가 푸는 문제

- 잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 하나의 흐름으로 묶어야 한다.
- 중복 요청과 동시 요청에서도 일관성을 유지해야 한다.
- 운영 기본 요소와 reproducibility까지 README 기준으로 설명할 수 있어야 한다.

## 내가 만든 답

- API server, purchase service, relay, repository, e2e tests를 `solution/go`에 구현했다.
- idempotency key, optimistic locking, outbox relay, rate limiting을 한 프로젝트 안에서 다시 조합했다.
- 문제 정의와 답안 요약, docs/notion을 분리해 제출 가능한 공개 표면을 정리한다.

## 핵심 설계 선택

- 필수 기술을 하나의 단일 백엔드 기준선으로 다시 묶어 capstone으로 삼았다.
- OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.

## 검증

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- `cd solution/go && go test ./...`
- `cd solution/go && make repro`

## 제외 범위

- 서비스 분리
- 복잡한 OAuth/외부 인증

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/04-platform-capstone/09-game-store-capstone (`legacy/04-platform-capstone/09-game-store-capstone/README.md`, public repo에는 미포함)

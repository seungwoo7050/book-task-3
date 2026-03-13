# 17 Game Store Capstone Series Map

`04-capstone/17-game-store-capstone`는 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다.

## 이 시리즈가 복원하는 것

- 시작점: 잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 하나의 흐름으로 묶어야 한다.
- 구현 축: API server, purchase service, relay, repository, e2e tests를 `solution/go`에 구현했다.
- 검증 축: 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 글 수: 4편

## 읽는 순서

- [10-bootstrap-and-schema.md](10-bootstrap-and-schema.md)
- [20-purchase-flow-and-tx-core.md](20-purchase-flow-and-tx-core.md)
- [30-relay-http-and-ops-surface.md](30-relay-http-and-ops-surface.md)
- [40-repro-and-e2e-hardening.md](40-repro-and-e2e-hardening.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.

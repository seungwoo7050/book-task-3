# commerce-backend 시리즈 지도

`commerce-backend`는 7개 랩에서 다룬 주제를 한 커머스 도메인으로 다시 묶은 baseline capstone이다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면 이 프로젝트의 목적은 가장 깊은 구현을 보여 주는 것이 아니라, 상품, 장바구니, 주문, 기본 인증 surface가 한 modular monolith 안에서 어떻게 만나는지 비교 기준을 만드는 데 있다.

## 이 프로젝트가 푸는 문제

- 랩별로 나뉘어 있던 auth, catalog, cart, order를 한 도메인으로 다시 조합한다.
- v2와 비교할 baseline을 만든다.
- 일부러 얕게 남긴 지점을 숨기지 않는다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `CommerceAuthController`, `CommerceService`, `CommerceController`
- `CommerceApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-assembling-the-baseline.md`
2. `20-checkout-proof-and-remaining-gaps.md`
3. `_evidence-ledger.md`
4. `_structure-outline.md`

## 시리즈의 중심 질문

- baseline capstone은 왜 깊이보다 비교 가능성을 우선하는가
- 상품, 장바구니, 주문은 어떤 최소 흐름으로 묶였는가
- v2에서 더 깊어질 축은 어디인가

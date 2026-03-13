# C-authorization-lab 시리즈 지도

`C-authorization-lab`은 "누구인가"를 확인하는 인증 다음에 "무엇을 할 수 있는가"를 따로 떼어 다룬다. macOS + VSCode 통합 터미널에서 `make test`를 직접 돌려 보면 이 랩의 핵심은 복잡한 policy engine이 아니라 organization, invitation, membership, role change를 코드와 테스트에서 선명하게 남기는 데 있다는 점이 보인다.

## 이 프로젝트가 푸는 문제

- organization과 membership lifecycle을 auth 랩과 분리해 설명한다.
- invite 발급과 수락, role 변경을 하나의 authorization baseline으로 만든다.
- persistence나 method security를 아직 붙이지 않아도 인가 규칙의 shape를 드러낸다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `AuthorizationDemoService`, `AuthorizationController`
- `AuthorizationApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈의 중심 질문

- authorization은 왜 auth 랩에 섞지 말아야 하는가
- invite 수락이 membership 상태를 어떻게 바꾸는가
- 다음 단계에서 method security를 붙일 자리는 어디인가

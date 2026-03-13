# B-federation-security-lab 시리즈 지도

`B-federation-security-lab`은 로컬 계정 인증 다음에 무엇이 붙는지를 다룬다. macOS + VSCode 통합 터미널에서 `make`와 `./gradlew`를 직접 호출하는 흐름을 기준으로 보면, 이 랩은 실제 Google provider를 붙이기 전에 authorize/callback contract, TOTP setup/verify, audit event를 먼저 고정하는 프로젝트다.

## 이 프로젝트가 푸는 문제

- 로컬 로그인만으로는 설명되지 않는 외부 identity 연동 경계를 어떻게 잘라 낼 것인가
- 2FA를 단순 숫자 맞추기가 아니라 setup, verify, recovery 관점으로 어떻게 보여 줄 것인가
- 인증 강화가 남기는 흔적을 audit event로 어떻게 설명할 것인가

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `FederationSecurityDemoService`, `FederationSecurityController`
- `FederationSecurityApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈의 중심 질문

- provider integration 없이도 federation 경계를 얼마나 선명하게 설명할 수 있는가
- 2FA와 audit를 왜 같은 랩에서 다루는가
- 다음 단계로 미뤄 둔 enforcement는 무엇인가

# A-auth-lab 시리즈 지도

`A-auth-lab`은 로컬 계정 인증에서 어디까지를 "기본 흐름"으로 볼지 먼저 고정한 뒤, 그 범위를 in-memory 서비스와 MockMvc 테스트로 닫는 랩이다. 작업 환경은 macOS + VSCode 통합 터미널이며, IntelliJ 실행 구성을 전제로 쓰지 않고 `make`와 `./gradlew`를 직접 호출하는 흐름으로 기록한다.

## 이 프로젝트가 푸는 문제

- 회원가입, 로그인, refresh, logout, `me`를 한 랩 안에서 설명 가능한 최소 인증 lifecycle로 묶는다.
- refresh rotation과 CSRF를 frontend 없이도 API 경계로 설명한다.
- 메일 검증, 비밀번호 재설정, OAuth 같은 확장 포인트는 현재 범위 바깥으로 남긴다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `AuthDemoService`, `AuthController`
- `AuthFlowApiTest`, `HealthApiTest`, `LabInfoApiSmokeTest`
- `2026-03-13` `make test` 재실행과 `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈에서 계속 붙드는 질문

- refresh token rotation은 왜 단순 재발급이 아니라 폐기와 재발급의 묶음이어야 하는가
- cookie를 완전히 붙이기 전에도 CSRF 경계를 어디까지 증명할 수 있는가
- 다음 랩으로 넘겨야 할 인증 강화 기능은 무엇인가

# A-auth-lab evidence ledger

- 복원 방식: 세밀한 작업 로그가 없어 `Phase 1 -> Phase 3` 순서로 다시 세웠다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `AuthDemoService.java`, `AuthFlowApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준. IntelliJ 전용 흐름은 쓰지 않았다.

## Phase 1

- 당시 목표: `register -> login -> refresh -> logout -> me`를 baseline auth 범위로 먼저 고정한다.
- 변경 단위: `README.md`, `problem/README.md`, `AuthFlowApiTest.java`
- 처음 가설: 로그인과 토큰 발급만 있어도 기본 인증 설명이 가능할 것 같았다.
- 실제 조치: 회원가입 뒤 로그인, refresh, `me` 조회를 한 테스트 흐름으로 묶었다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `AuthFlowApiTest` 2개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `AuthFlowApiTest.registerLoginAndRefreshFlowWorks()`
- 새로 배운 것: baseline auth의 첫 기준은 storage depth가 아니라 lifecycle 전체를 설명할 수 있는 API shape다.
- 다음: refresh rotation과 CSRF 경계를 서비스 코드에서 분리한다.

## Phase 2

- 당시 목표: refresh rotation과 CSRF mismatch를 baseline auth 안으로 넣을지 결정한다.
- 변경 단위: `AuthDemoService.java`
- 처음 가설: refresh token을 재사용해도 충분할 수 있다고 봤다.
- 실제 조치: `refresh()`에서 기존 세션을 제거하고 새 refresh token과 CSRF token을 만들었다. `requireSession()`에서 CSRF mismatch를 즉시 끊었다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `AuthDemoService.refresh()`, `AuthDemoService.requireSession()`
- 새로 배운 것: refresh rotation은 액세스 토큰 재발급이 아니라 세션 재생산 규칙이다.
- 다음: persistence를 얕게 둔 이유와 현재 한계를 문서에 고정한다.

## Phase 3

- 당시 목표: 지금 증명한 범위와 아직 남긴 범위를 분명히 닫는다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.AuthFlowApiTest.xml`
- 처음 가설: 기능만 있으면 문서는 짧아도 충분할 것 같았다.
- 실제 조치: Mailpit-ready 환경, cookie + CSRF 경계, persistence 미구현 범위를 docs와 검증 기록에 남겼다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 6개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: 이 랩의 핵심은 기능 확장이 아니라 baseline 경계를 먼저 닫는 일이다.
- 다음: federation, 2FA, audit는 `B-federation-security-lab`로 넘긴다.

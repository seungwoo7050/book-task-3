# B-federation-security-lab evidence ledger

- 복원 방식: 세밀한 세션 기록이 없어 `Phase 1 -> Phase 3` 순서로 복원했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `FederationSecurityDemoService.java`, `FederationSecurityApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: federation, 2FA, audit를 하나의 인증 강화 랩으로 자른다.
- 변경 단위: `README.md`, `problem/README.md`, `FederationSecurityApiTest.java`
- 처음 가설: live Google provider가 있어야 federation 랩이 성립할 것 같았다.
- 실제 조치: `authorize`, `callback`, audit 조회를 먼저 테스트로 고정했다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `FederationSecurityApiTest` 2개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `FederationSecurityApiTest.googleCallbackAndAuditFlowWork()`
- 새로 배운 것: federation의 첫 증명 대상은 live provider가 아니라 callback contract다.
- 다음: TOTP와 audit를 같은 상태 변화로 묶는다.

## Phase 2

- 당시 목표: OAuth callback, TOTP, recovery code, audit를 같은 흐름으로 읽히게 만든다.
- 변경 단위: `FederationSecurityDemoService.java`
- 처음 가설: 2FA는 federation과 따로 떼는 편이 자연스러워 보였다.
- 실제 조치: `authorize()`, `callback()`, `setupTotp()`, `verifyTotp()`를 한 서비스에 두고 audit event를 매 단계에 남겼다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `FederationSecurityDemoService.authorize()`, `setupTotp()`, `verifyTotp()`
- 새로 배운 것: 인증 강화는 기능 목록이 아니라 state와 흔적을 함께 남기는 흐름이다.
- 다음: 실제 provider 미연동과 rate limiting 미구현을 docs에 명시한다.

## Phase 3

- 당시 목표: 지금 구현한 security hardening과 다음 단계 범위를 분리해 닫는다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.FederationSecurityApiTest.xml`
- 처음 가설: 기능이 보이면 한계는 자연스럽게 읽힐 줄 알았다.
- 실제 조치: contract-level Google 연동, 단순화된 TOTP, 미구현 rate limiting을 문서에 명시했다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 6개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: security 랩은 구현한 기능만큼 남겨 둔 한계를 같이 적어야 과장되지 않는다.
- 다음: authorization은 `C-authorization-lab`에서 별도 문제로 분리한다.

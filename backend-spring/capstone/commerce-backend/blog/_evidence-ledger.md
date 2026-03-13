# commerce-backend evidence ledger

- 복원 방식: 세밀한 commit chronology 대신 `Phase 1 -> Phase 3`으로 통합 흐름을 복원했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `CommerceApiTest.java`, `CommerceService.java`, `CommerceAuthController.java`, `V2__commerce.sql`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: 여러 랩 학습을 하나의 커머스 API 흐름으로 다시 묶는다.
- 변경 단위: `README.md`, `problem/README.md`, `CommerceApiTest.java`
- 처음 가설: 랩 코드를 그대로 조합해도 첫 캡스톤으로 충분할 수 있다고 봤다.
- 실제 조치: 로그인, 상품 생성/조회, 장바구니 추가, 주문 생성, 관리자 주문 조회를 한 테스트에 묶었다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `CommerceApiTest` 1개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `CommerceApiTest.catalogCartAndOrderFlowWork()`
- 새로 배운 것: 첫 캡스톤의 핵심은 기능 깊이보다 통합 surface를 만드는 일이다.
- 다음: modular monolith baseline을 schema와 서비스 코드에 연결한다.

## Phase 2

- 당시 목표: auth, catalog, cart, order를 얕지만 일관된 modular monolith로 묶는다.
- 변경 단위: `V2__commerce.sql`, `CommerceService.java`, `CommerceAuthController.java`
- 처음 가설: 첫 통합 캡스톤에서도 persisted auth나 payment까지 바로 넣어야 할 것 같았다.
- 실제 조치: auth는 contract-level login과 `me`로 가볍게 두고, 상품/장바구니/주문과 stock decrement를 먼저 연결했다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `V2__commerce.sql`, `CommerceService.checkout()`, `CommerceAuthController.login()`
- 새로 배운 것: baseline capstone은 깊이 부족이 아니라 비교 기준점이라는 역할을 가져야 한다.
- 다음: payment와 persisted auth를 비워 둔 이유를 docs에 남긴다.

## Phase 3

- 당시 목표: 이 버전이 최종 답이 아니라 baseline이라는 점을 분명히 닫는다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.CommerceApiTest.xml`
- 처음 가설: 통합 도메인만 보이면 왜 v2가 필요한지 자연스럽게 읽힐 줄 알았다.
- 실제 조치: auth depth 부족, payment 없음, notification/event consumer 미완을 docs와 검증 기록에 남겼다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 5개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 baseline 설명, `verification-report.md`
- 새로 배운 것: 일부러 남긴 빈칸이 있어야 다음 버전의 개선 축이 분명해진다.
- 다음: 같은 도메인을 더 깊게 푼 `commerce-backend-v2`로 넘어간다.

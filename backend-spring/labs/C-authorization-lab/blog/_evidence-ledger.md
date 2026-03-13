# C-authorization-lab evidence ledger

- 복원 방식: 작업 로그가 부족해 `Phase 1 -> Phase 3` 순서로 다시 정리했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `AuthorizationDemoService.java`, `AuthorizationApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: authorization을 organization, invite, membership, role 변경 문제로 작게 자른다.
- 변경 단위: `README.md`, `problem/README.md`, `AuthorizationApiTest.java`
- 처음 가설: method security나 policy engine부터 들어가야 할 것 같았다.
- 실제 조치: 조직 생성, 초대, 수락, role 변경을 한 테스트 시나리오로 고정했다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `AuthorizationApiTest` 1개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `AuthorizationApiTest.inviteAcceptAndRoleChangeFlowWork()`
- 새로 배운 것: authorization의 첫 기준은 어노테이션보다 membership lifecycle이다.
- 다음: owner, pending, accepted 전이를 서비스 코드에 명시한다.

## Phase 2

- 당시 목표: invite와 membership 전이를 in-memory state로라도 분명하게 남긴다.
- 변경 단위: `AuthorizationDemoService.java`
- 처음 가설: persistence가 없으면 인가 규칙이 너무 약해 보일 수 있다고 생각했다.
- 실제 조치: 조직 생성 시 owner를 넣고, invite 시 `PENDING`, accept 시 실제 role로 바꿨다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `AuthorizationDemoService.createOrganization()`, `invite()`, `accept()`
- 새로 배운 것: authorization에서는 storage 기술보다 state transition을 먼저 드러내는 편이 설명력이 높다.
- 다음: method security를 미룬 이유와 현재 한계를 docs에 고정한다.

## Phase 3

- 당시 목표: policy engine이 아니라 service-logic baseline이라는 점을 닫는다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.AuthorizationApiTest.xml`
- 처음 가설: role 변경 API만 보이면 충분할 것 같았다.
- 실제 조치: method security 미적용, in-memory membership, 최소 ownership check라는 한계를 문서에 남겼다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 5개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: baseline authorization은 정교한 enforcement보다 규칙의 위치를 먼저 드러내는 편이 낫다.
- 다음: persistence 선택은 `D-data-jpa-lab`에서 본격적으로 다룬다.

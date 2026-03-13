# D-data-jpa-lab evidence ledger

- 복원 방식: 세부 세션 로그 대신 `Phase 1 -> Phase 3` 흐름으로 다시 세웠다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `DataApiService.java`, `ProductEntity.java`, `V2__lab_products.sql`, `DataApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: JPA 랩을 CRUD가 아니라 persistence 선택을 설명하는 랩으로 자른다.
- 변경 단위: `README.md`, `problem/README.md`, `DataApiTest.java`
- 처음 가설: create/list/update 정도면 JPA 랩 범위를 설명할 수 있을 것 같았다.
- 실제 조치: product 생성, 목록 조회, price 수정, version conflict를 한 테스트에 묶었다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `DataApiTest` 1개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `DataApiTest.productCrudAndConflictCheckWork()`
- 새로 배운 것: JPA 랩의 핵심은 엔드포인트 개수보다 충돌 지점을 어디에 두는가다.
- 다음: Flyway schema와 `@Version`을 서비스 코드와 연결한다.

## Phase 2

- 당시 목표: migration, entity, optimistic-lock-style check를 한 이야기로 묶는다.
- 변경 단위: `V2__lab_products.sql`, `ProductEntity.java`, `DataApiService.java`
- 처음 가설: JPA가 동작하면 schema migration은 글에서 비중이 작아도 될 것 같았다.
- 실제 조치: `lab_products` 테이블에 `version` 컬럼을 두고, entity와 `updatePrice()`의 version check를 연결했다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `V2__lab_products.sql`, `ProductEntity.version`, `DataApiService.updatePrice()`
- 새로 배운 것: JPA는 repository 호출보다 schema -> entity -> service guard가 한 줄로 이어질 때 설계 선택으로 읽힌다.
- 다음: Querydsl과 larger graph를 아직 뒤로 미룬 이유를 문서에 고정한다.

## Phase 3

- 당시 목표: 지금 증명한 persistence 범위와 다음 단계 범위를 분명히 나눈다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.DataApiTest.xml`
- 처음 가설: conflict check만 있으면 JPA 선택의 의미가 충분히 보일 줄 알았다.
- 실제 조치: Querydsl은 구조만 준비했고 soft delete와 larger graph는 다음 단계라고 docs에 적었다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 5개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: JPA 랩은 무엇을 더 구현하지 않았는지까지 적어야 CRUD 데모로 흐르지 않는다.
- 다음: DB와 메시지 경계는 `E-event-messaging-lab`으로 이어진다.

# D-data-jpa-lab 시리즈 지도

`D-data-jpa-lab`은 JPA를 "저장만 되면 끝"인 도구로 다루지 않는다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면 이 랩의 핵심은 Flyway, entity, repository, service, pagination, optimistic locking을 한 흐름으로 묶어 JPA의 선택 지점을 설명하는 데 있다.

## 이 프로젝트가 푸는 문제

- JPA를 persistence choice와 version 관리가 드러나는 코드로 만든다.
- pagination과 optimistic locking을 API 수준에서 설명한다.
- Querydsl은 구조만 준비하고 아직 심화하지 않는다.

## 이 시리즈의 근거

- `problem/README.md`
- `docs/README.md`
- `spring/README.md`
- `ProductEntity`, `ProductRepository`, `DataApiService`
- `DataApiTest`
- `2026-03-13` `make test` 재실행, `2026-03-09` 검증 보고

## 읽는 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-outline.md`

## 시리즈의 중심 질문

- version을 왜 API 요청값으로 함께 받아야 하는가
- JPA 경계는 어떤 파일 배치와 테스트로 설명되는가
- 지금 남겨 둔 Querydsl 확장은 어디서 시작하면 되는가

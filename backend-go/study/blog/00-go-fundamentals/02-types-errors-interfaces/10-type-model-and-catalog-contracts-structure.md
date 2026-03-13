# 02 Types Errors Interfaces Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 가격 계산 규칙을 interface로 분리해 concrete type과 정책 객체의 경계를 드러냈다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `00-go-fundamentals/02-types-errors-interfaces` 안에서 `10-type-model-and-catalog-contracts.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 도메인 타입 정의 -> Phase 3: Catalog 구현 -> Phase 4: CLI 바이너리 작성 -> Phase 5: 테스트 작성 및 검증 -> Phase 6: 문서 작성 및 최종 검증
- 세션 본문: `lesson/, domain/, solution/go/domain/catalog.go, solution/go/cmd/inventorydemo/main.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/domain/catalog.go`
- 코드 앵커 2: `solution/go/domain/catalog_test.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: struct는 상태를, method는 그 상태에 대한 동작을 표현한다.
- 마지막 단락: 외부 저장소나 persistence 계층은 포함하지 않았다.

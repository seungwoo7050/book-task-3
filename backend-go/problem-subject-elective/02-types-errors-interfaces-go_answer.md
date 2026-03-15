# 02-types-errors-interfaces-go 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 SKU 중복 추가를 막는다, 존재하지 않는 상품 조회 시 custom error를 반환한다, 할인 규칙을 interface로 분리한다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `Apply`, `Error` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- SKU 중복 추가를 막는다.
- 존재하지 않는 상품 조회 시 custom error를 반환한다.
- 할인 규칙을 interface로 분리한다.
- 첫 진입점은 `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/cmd/inventorydemo/main.go`이고, 여기서 `main`와 `Apply` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/cmd/inventorydemo/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/domain/catalog.go`: `Apply`, `Error`, `NewCatalog`, `Add`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/domain/catalog_test.go`: `TestCatalogAddDuplicate`, `TestCatalogFinalPrice`, `TestCatalogGetNotFound`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/go.mod`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `main` 구현은 `TestCatalogAddDuplicate` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/go.mod`는 실행 루트와 모듈 경계를 고정해 검증이 어느 위치에서 돌아야 하는지 알려 준다.

## 정답을 재구성하는 절차

1. `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/cmd/inventorydemo/main.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestCatalogAddDuplicate` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestCatalogAddDuplicate`와 `TestCatalogFinalPrice`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/cmd/inventorydemo/main.go`
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/domain/catalog.go`
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/domain/catalog_test.go`
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/go.mod`

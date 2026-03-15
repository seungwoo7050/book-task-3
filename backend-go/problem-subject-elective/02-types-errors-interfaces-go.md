# 02-types-errors-interfaces-go 문제지

## 왜 중요한가

작은 상품 카탈로그를 만들고, struct와 interface를 사용해 가격 계산 규칙을 분리한다.

## 목표

시작 위치의 구현을 완성해 SKU 중복 추가를 막는다, 존재하지 않는 상품 조회 시 custom error를 반환한다, 할인 규칙을 interface로 분리한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/cmd/inventorydemo/main.go`
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/domain/catalog.go`
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/domain/catalog_test.go`
- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/go.mod`

## starter code / 입력 계약

- `../study/00-go-fundamentals/02-types-errors-interfaces/solution/go/cmd/inventorydemo/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- SKU 중복 추가를 막는다.
- 존재하지 않는 상품 조회 시 custom error를 반환한다.
- 할인 규칙을 interface로 분리한다.

## 제외 범위

- DB 연동
- mock 프레임워크 활용
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `Apply`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestCatalogAddDuplicate`와 `TestCatalogFinalPrice`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/00-go-fundamentals/02-types-errors-interfaces/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-types-errors-interfaces-go_answer.md`](02-types-errors-interfaces-go_answer.md)에서 확인한다.

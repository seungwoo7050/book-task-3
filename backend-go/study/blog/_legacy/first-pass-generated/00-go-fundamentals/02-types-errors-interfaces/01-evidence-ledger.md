# 02 Types Errors Interfaces Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: struct, method, interface, custom error를 작은 상품 카탈로그로 묶어 타입 감각을 붙이는 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/domain/catalog.go`, `solution/go/domain/catalog_test.go`
- 대표 검증 명령: `cd solution/go && go run ./cmd/inventorydemo`, `cd solution/go && go test ./...`
- 핵심 개념 축: `struct는 상태를, method는 그 상태에 대한 동작을 표현한다.`, `interface는 “무엇을 할 수 있는가”를 분리할 때만 쓰는 편이 단순하다.`, custom error 타입은 `errors.As`로 세부 의미를 복원할 수 있게 해 준다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - Catalog와 custom error로 도메인 규칙을 먼저 세운다

        - 당시 목표: Catalog와 custom error로 도메인 규칙을 먼저 세운다
        - 변경 단위: `solution/go/domain/catalog.go`의 `NewCatalog`
        - 처음 가설: `NewCatalog`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
        - 실제 조치: `solution/go/domain/catalog.go`의 `NewCatalog`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
        - CLI: `cd solution/go && go run ./cmd/inventorydemo`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `starter-pack final price: 2400 cents`였다.
        - 핵심 코드 앵커:
        - `NewCatalog`: `solution/go/domain/catalog.go`

        ```go
        func NewCatalog() *Catalog {
	return &Catalog{items: make(map[string]Item)}
}

func (c *Catalog) Add(item Item) error {
	if _, exists := c.items[item.SKU]; exists {
		return ErrDuplicateSKU
	}
	c.items[item.SKU] = item
        ```

        - 새로 배운 것: struct는 상태를, method는 그 상태에 대한 동작을 표현한다.
        - 다음: PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다
        ### 2. Phase 2 - PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다

        - 당시 목표: PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다
        - 변경 단위: `solution/go/domain/catalog.go`의 `PercentageDiscount.Apply`
        - 처음 가설: `PercentageDiscount.Apply`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
        - 실제 조치: `solution/go/domain/catalog.go`의 `PercentageDiscount.Apply`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/cmd/inventorydemo	[no test files]`였다.
        - 핵심 코드 앵커:
        - `PercentageDiscount.Apply`: `solution/go/domain/catalog.go`

        ```go
        func (d PercentageDiscount) Apply(priceCents int) int {
	if d.Percent <= 0 {
		return priceCents
	}
	return priceCents - (priceCents*d.Percent)/100
}

type NotFoundError struct {
	SKU string
        ```

        - 새로 배운 것: sentinel error는 비교가 쉽지만 문맥이 약하다. custom error는 문맥이 풍부하지만 타입 관리가 필요하다.
        - 다음: catalog_test로 duplicate, not-found, final price 계약을 잠근다
        ### 3. Phase 3 - catalog_test로 duplicate, not-found, final price 계약을 잠근다

        - 당시 목표: catalog_test로 duplicate, not-found, final price 계약을 잠근다
        - 변경 단위: `solution/go/domain/catalog_test.go`의 `TestCatalogFinalPrice`
        - 처음 가설: 테스트 이름 `TestCatalogFinalPrice`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
        - 실제 조치: `solution/go/domain/catalog_test.go`의 `TestCatalogFinalPrice`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/cmd/inventorydemo	[no test files]`였다.
        - 핵심 코드 앵커:
        - `TestCatalogFinalPrice`: `solution/go/domain/catalog_test.go`

        ```go
        func TestCatalogFinalPrice(t *testing.T) {
	t.Parallel()

	catalog := NewCatalog()
	if err := catalog.Add(Item{SKU: "sku-2", Name: "Shield", PriceCents: 2000}); err != nil {
		t.Fatalf("add error: %v", err)
	}
	price, err := catalog.FinalPrice("sku-2", PercentageDiscount{Percent: 10})
	if err != nil {
        ```

        - 새로 배운 것: pointer/value receiver를 뒤섞으면 상태 변경 의도가 흐려진다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/02-types-errors-interfaces && cd solution/go && go run ./cmd/inventorydemo)
```

```text
starter-pack final price: 2400 cents
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/02-types-errors-interfaces && cd solution/go && go test ./...)
```

```text
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/cmd/inventorydemo	[no test files]
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/domain	(cached)
```

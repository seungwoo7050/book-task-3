# 02 Types Errors Interfaces 재구성 개발 로그

02 Types Errors Interfaces는 struct, method, interface, custom error를 작은 상품 카탈로그로 묶어 타입 감각을 붙이는 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: Catalog와 custom error로 도메인 규칙을 먼저 세운다 - `solution/go/domain/catalog.go`의 `NewCatalog`
- Phase 2: PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다 - `solution/go/domain/catalog.go`의 `PercentageDiscount.Apply`
- Phase 3: catalog_test로 duplicate, not-found, final price 계약을 잠근다 - `solution/go/domain/catalog_test.go`의 `TestCatalogFinalPrice`

                ## Phase 1. Catalog와 custom error로 도메인 규칙을 먼저 세운다

        - 당시 목표: Catalog와 custom error로 도메인 규칙을 먼저 세운다
        - 변경 단위: `solution/go/domain/catalog.go`의 `NewCatalog`
        - 처음 가설: `NewCatalog`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
        - 실제 진행: `solution/go/domain/catalog.go`의 `NewCatalog`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
        - CLI: `cd solution/go && go run ./cmd/inventorydemo`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `starter-pack final price: 2400 cents`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `NewCatalog`는 `solution/go/domain/catalog.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: struct는 상태를, method는 그 상태에 대한 동작을 표현한다.
        - 다음: PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다
        ## Phase 2. PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다

        - 당시 목표: PricingRule과 inventorydemo CLI로 할인 계산 경로를 연결한다
        - 변경 단위: `solution/go/domain/catalog.go`의 `PercentageDiscount.Apply`
        - 처음 가설: `PercentageDiscount.Apply`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
        - 실제 진행: `solution/go/domain/catalog.go`의 `PercentageDiscount.Apply`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/cmd/inventorydemo	[no test files]`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `PercentageDiscount.Apply`는 `solution/go/domain/catalog.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: sentinel error는 비교가 쉽지만 문맥이 약하다. custom error는 문맥이 풍부하지만 타입 관리가 필요하다.
        - 다음: catalog_test로 duplicate, not-found, final price 계약을 잠근다
        ## Phase 3. catalog_test로 duplicate, not-found, final price 계약을 잠근다

        - 당시 목표: catalog_test로 duplicate, not-found, final price 계약을 잠근다
        - 변경 단위: `solution/go/domain/catalog_test.go`의 `TestCatalogFinalPrice`
        - 처음 가설: 테스트 이름 `TestCatalogFinalPrice`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
        - 실제 진행: `solution/go/domain/catalog_test.go`의 `TestCatalogFinalPrice`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/cmd/inventorydemo	[no test files]`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `TestCatalogFinalPrice`는 `solution/go/domain/catalog_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: pointer/value receiver를 뒤섞으면 상태 변경 의도가 흐려진다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/02-types-errors-interfaces && cd solution/go && go run ./cmd/inventorydemo)
```

```text
starter-pack final price: 2400 cents
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/00-go-fundamentals/02-types-errors-interfaces && cd solution/go && go test ./...)
```

```text
?   	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/cmd/inventorydemo	[no test files]
ok  	github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces/domain	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: `struct는 상태를, method는 그 상태에 대한 동작을 표현한다.`, `interface는 “무엇을 할 수 있는가”를 분리할 때만 쓰는 편이 단순하다.`, custom error 타입은 `errors.As`로 세부 의미를 복원할 수 있게 해 준다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: struct, method, interface, custom error를 카탈로그 가격 계산이라는 한 문제로 묶는다.

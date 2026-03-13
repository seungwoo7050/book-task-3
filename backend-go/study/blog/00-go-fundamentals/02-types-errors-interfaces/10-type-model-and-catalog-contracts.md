# 02 Types Errors Interfaces — Type Model And Catalog Contracts

`00-go-fundamentals/02-types-errors-interfaces`는 struct, method, interface, custom error를 작은 상품 카탈로그로 묶어 타입 감각을 붙이는 과제다. 이 글에서는 Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 도메인 타입 정의 -> Phase 3: Catalog 구현 -> Phase 4: CLI 바이너리 작성 -> Phase 5: 테스트 작성 및 검증 -> Phase 6: 문서 작성 및 최종 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 1: 프로젝트 뼈대 만들기
- Phase 2: 도메인 타입 정의
- Phase 3: Catalog 구현
- Phase 4: CLI 바이너리 작성
- Phase 5: 테스트 작성 및 검증
- Phase 6: 문서 작성 및 최종 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `lesson/`, `domain/`, `solution/go/domain/catalog.go`, `solution/go/cmd/inventorydemo/main.go`, `solution/go/domain/catalog_test.go`, `problem/README.md`
- 처음 가설: 가격 계산 규칙을 interface로 분리해 concrete type과 정책 객체의 경계를 드러냈다.
- 실제 진행: 디렉터리 구조 생성 프로젝트 01과 같은 구조를 따르되, 도메인 로직 패키지 이름을 `lesson/` 대신 `domain/`으로 바꿨다. "카탈로그"라는 도메인 개념이 있으니 패키지 이름도 그에 맞춘 것이다. Item struct 작성 (`solution/go/domain/catalog.go`) 가장 먼저 `Item` struct를 정의했다. 세 필드: SKU(문자열), Name(문자열), PriceCents(정수). 가격을 센트 단위로 한 건 부동소수점 오차를 피하기 위해서다.

CLI:

```bash
mkdir -p 00-go-fundamentals/02-types-errors-interfaces/{solution/go/cmd/inventorydemo,solution/go/domain,docs/concepts,docs/references,problem}

cd 00-go-fundamentals/02-types-errors-interfaces/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces
```

검증 신호:

- Catalog을 생성하고 상품 하나를 추가한 뒤 20% 할인된 가격을 출력한다. `log.Fatal`로 에러를 처리한다.
- 출력: starter-pack final price: 2400 cents
- ok   .../02-types-errors-interfaces/domain
- --- PASS: TestCatalogAddDuplicate (0.00s)
- --- PASS: TestCatalogFinalPrice (0.00s)

핵심 코드: `solution/go/domain/catalog.go`

```go
var ErrDuplicateSKU = errors.New("duplicate sku")

type Item struct {
	SKU        string
	Name       string
	PriceCents int
}

type PricingRule interface {
	Apply(priceCents int) int
}

type PercentageDiscount struct {
	Percent int
}

func (d PercentageDiscount) Apply(priceCents int) int {
	if d.Percent <= 0 {
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- struct는 상태를, method는 그 상태에 대한 동작을 표현한다.

보조 코드: `solution/go/domain/catalog_test.go`

```go
func TestCatalogAddDuplicate(t *testing.T) {
	t.Parallel()

	catalog := NewCatalog()
	item := Item{SKU: "sku-1", Name: "Sword", PriceCents: 1500}
	if err := catalog.Add(item); err != nil {
		t.Fatalf("unexpected add error: %v", err)
	}
	if err := catalog.Add(item); !errors.Is(err, ErrDuplicateSKU) {
		t.Fatalf("duplicate add error = %v, want %v", err, ErrDuplicateSKU)
	}
}

func TestCatalogFinalPrice(t *testing.T) {
	t.Parallel()

	catalog := NewCatalog()
	if err := catalog.Add(Item{SKU: "sku-2", Name: "Shield", PriceCents: 2000}); err != nil {
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

CLI:

```bash
cd 00-go-fundamentals/02-types-errors-interfaces/go
go run ./cmd/inventorydemo
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go run ./cmd/inventorydemo`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.

다음:

- 외부 저장소나 persistence 계층은 포함하지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/domain/catalog.go` 같은 결정적인 코드와 `cd 00-go-fundamentals/02-types-errors-interfaces/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.

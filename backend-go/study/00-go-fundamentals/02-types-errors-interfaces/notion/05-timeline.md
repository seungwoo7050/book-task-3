# 개발 타임라인 — 처음부터 끝까지

이 문서는 프로젝트 02를 처음부터 완성까지 만드는 전체 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 뼈대 만들기

### 1-1. 디렉터리 구조 생성

```bash
mkdir -p 00-go-fundamentals/02-types-errors-interfaces/{go/cmd/inventorydemo,go/domain,docs/concepts,docs/references,problem}
```

프로젝트 01과 같은 구조를 따르되, 도메인 로직 패키지 이름을 `lesson/` 대신 `domain/`으로 바꿨다. "카탈로그"라는 도메인 개념이 있으니 패키지 이름도 그에 맞춘 것이다.

### 1-2. Go 모듈 초기화

```bash
cd 00-go-fundamentals/02-types-errors-interfaces/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces
```

Go 1.22, 외부 의존성 없음.

### 1-3. Workspace 등록

```bash
cd study
go work use 00-go-fundamentals/02-types-errors-interfaces/go
```

---

## Phase 2: 도메인 타입 정의

### 2-1. Item struct 작성 (`go/domain/catalog.go`)

가장 먼저 `Item` struct를 정의했다. 세 필드: SKU(문자열), Name(문자열), PriceCents(정수). 가격을 센트 단위로 한 건 부동소수점 오차를 피하기 위해서다.

### 2-2. 에러 정의

같은 파일에 두 종류의 에러를 정의했다:
- `ErrDuplicateSKU` — `errors.New("duplicate sku")`로 sentinel error 생성
- `NotFoundError` — SKU를 담는 struct, `Error() string` 메서드를 구현해서 `error` interface를 충족

### 2-3. PricingRule interface 정의

```go
type PricingRule interface {
    Apply(priceCents int) int
}
```

메서드 하나짜리 interface. `PercentageDiscount` struct가 이걸 구현한다.

---

## Phase 3: Catalog 구현

### 3-1. Catalog struct와 생성자

`Catalog`은 `map[string]Item`을 내부에 가진다. `NewCatalog()`에서 map을 초기화한다.

### 3-2. Add 메서드 (pointer receiver)

SKU 중복 체크 후 map에 추가. 중복이면 `ErrDuplicateSKU` 반환. pointer receiver를 사용하는 이유는 map에 항목을 변경하기 때문이다.

### 3-3. Get 메서드

map에서 SKU로 조회. 없으면 `NotFoundError{SKU: sku}` 반환.

### 3-4. FinalPrice 메서드

`Get`으로 조회 → `PricingRule.Apply`로 할인 적용. rule이 nil이면 원래 가격 반환. 이 함수가 struct, method, interface, error를 모두 엮는 합류 지점이다.

---

## Phase 4: CLI 바이너리 작성

### 4-1. main.go 작성 (`go/cmd/inventorydemo/main.go`)

Catalog을 생성하고 상품 하나를 추가한 뒤 20% 할인된 가격을 출력한다. `log.Fatal`로 에러를 처리한다.

### 4-2. 첫 실행

```bash
cd go
go run ./cmd/inventorydemo
# 출력: starter-pack final price: 2400 cents
```

3000센트에서 20% 할인하면 2400센트. 손으로 계산한 값과 일치하는지 확인했다.

---

## Phase 5: 테스트 작성 및 검증

### 5-1. 테스트 파일 작성 (`go/domain/catalog_test.go`)

세 가지 테스트:

| 테스트 | 검증 대상 |
|--------|-----------|
| `TestCatalogAddDuplicate` | 중복 추가 시 `ErrDuplicateSKU` 반환, `errors.Is`로 검증 |
| `TestCatalogFinalPrice` | 10% 할인 적용 결과가 1800인지 확인 |
| `TestCatalogGetNotFound` | 없는 SKU 조회 시 `NotFoundError` 반환, `errors.As`로 검증 |

모든 테스트에 `t.Parallel()` 적용.

### 5-2. 테스트 실행

```bash
cd go
go test ./...
# ok   .../02-types-errors-interfaces/domain

go test -v ./domain/
# === RUN   TestCatalogAddDuplicate
# --- PASS: TestCatalogAddDuplicate (0.00s)
# === RUN   TestCatalogFinalPrice
# --- PASS: TestCatalogFinalPrice (0.00s)
# === RUN   TestCatalogGetNotFound
# --- PASS: TestCatalogGetNotFound (0.00s)
```

---

## Phase 6: 문서 작성 및 최종 검증

### 6-1. 문서 파일들

| 파일 | 내용 |
|------|------|
| `problem/README.md` | 과제 명세: 요구사항 3개 |
| `go/README.md` | 구현 모듈 요약 |
| `docs/README.md` | 문서 폴더 개요 |
| `docs/concepts/core-concepts.md` | struct/interface/error 핵심 개념 |
| `docs/references/README.md` | 참고 자료 |
| `docs/verification.md` | 검증 기록 |
| `README.md` | 프로젝트 루트 README |

### 6-2. Makefile 검증

```bash
cd study
make test-new
# ==> 00-go-fundamentals/02-types-errors-interfaces/go
# ok   ...
make check-docs
```

### 6-3. 상태 확정

`verified` 상태로 변경.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.22+ | 컴파일, 실행, 테스트 |
| `go mod init` | 모듈 초기화 |
| `go work use` | workspace에 모듈 등록 |
| `go run` | CLI 실행 |
| `go test` | 단위 테스트 |
| `make` | 전체 검증 |

외부 패키지 없음. Docker나 데이터베이스 의존성 없음.

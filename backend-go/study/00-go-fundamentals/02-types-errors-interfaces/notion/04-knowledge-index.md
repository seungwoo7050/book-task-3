# 지식 인덱스 — 빠른 참조용

## 에러 패턴

| 패턴 | 언제 사용 | 비교 방법 |
|------|-----------|-----------|
| Sentinel error | 에러 종류만 판단 | `errors.Is(err, ErrDuplicateSKU)` |
| Custom error 타입 | 에러에서 맥락 정보 추출 | `errors.As(err, &notFound)` |

## Receiver 선택 기준

| receiver | 언제 사용 | 이 과제 예시 |
|----------|-----------|-------------|
| Pointer (`*T`) | 내부 상태 변경 | `(c *Catalog) Add`, `(c *Catalog) Get` |
| Value (`T`) | 읽기 전용, 불변 | `(d PercentageDiscount) Apply` |

## 타입 구조

```
Item          — SKU, Name, PriceCents
Catalog       — map[string]Item (pointer receiver methods)
PricingRule   — interface { Apply(int) int }
PercentageDiscount — PricingRule 구현체
NotFoundError — custom error (SKU 포함)
ErrDuplicateSKU — sentinel error
```

## CLI 명령 정리

```bash
# 모듈 초기화
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces

# 실행
cd solution/go
go run ./cmd/inventorydemo
# 출력: starter-pack final price: 2400 cents

# 테스트
cd solution/go
go test ./...
go test -v ./domain/
go test -run TestCatalogGetNotFound ./domain/
```

## 참고 자료

- [Effective Go — Interfaces](https://go.dev/doc/effective_go#interfaces)
- [Go Blog — Error handling and Go](https://go.dev/blog/error-handling-and-go)
- [errors.Is vs errors.As](https://pkg.go.dev/errors)

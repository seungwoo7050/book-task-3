# 접근 과정 — 타입부터 세우고 행동을 붙이기까지

## Item struct에서 시작

가장 먼저 만든 건 `Item` struct였다. SKU, 이름, 가격(센트 단위) 세 필드다. 가격을 센트 단위 정수로 둔 건 Go에서 돈을 float로 다루면 소수점 오차 문제가 생기기 때문이다. 이건 Go에 국한된 문제가 아니라, 거의 모든 언어에서 통하는 관례다.

```go
type Item struct {
    SKU        string
    Name       string
    PriceCents int
}
```

## Catalog — map을 감싼 struct

`Catalog`은 `map[string]Item`을 내부에 가지고 있다. 왜 map을 그냥 노출하지 않고 struct로 감쌌느냐면, `Add`와 `Get`에서 에러를 반환하는 로직을 메서드로 깔끔하게 붙이기 위해서다.

`NewCatalog()` 생성자 함수를 만든 이유도 같다. Go에서 struct를 `&Catalog{}`로 직접 만들면 내부 map이 nil이라 panic이 난다. 생성자에서 `make(map[string]Item)`을 호출해 주는 게 안전한 초기화 패턴이다.

## 에러를 두 종류로 나눈 이유

에러를 하나로 통일하지 않고 두 종류로 나눈 건 의도적이었다:

1. **`ErrDuplicateSKU`** (sentinel error) — `errors.New`로 만든 패키지 수준 변수. 값 자체로 비교할 수 있어서 `errors.Is(err, ErrDuplicateSKU)` 한 줄로 판단이 끝난다.

2. **`NotFoundError`** (custom error 타입) — SKU 정보를 담고 있는 struct. `errors.As(err, &notFound)`로 에러를 구체 타입으로 복원해서 어떤 SKU가 없었는지 꺼낼 수 있다.

처음에는 둘 다 sentinel error로 하려 했다. 그런데 "어떤 SKU를 찾으려다 실패했는지"를 에러 메시지에 넣으려면 struct 타입이 필요했다. 이 차이를 입문자가 직접 경험하게 만드는 게 이 과제의 핵심 학습 포인트다.

## PricingRule interface

```go
type PricingRule interface {
    Apply(priceCents int) int
}
```

interface에 메서드가 하나밖에 없다. Go에서는 이게 권장 패턴이다. interface가 작을수록 구현하기 쉽고, 테스트용 mock을 만들기도 쉽다.

`PercentageDiscount` struct가 `Apply`를 구현한다. value receiver를 썼는데, 이 struct는 내부 상태를 변경할 필요가 없기 때문이다. 반면 `Catalog`의 `Add`는 pointer receiver를 쓴다—map에 항목을 추가하는 건 상태를 변경하는 행위니까.

이 두 가지를 같은 코드베이스에서 나란히 보여주면, receiver 선택 기준이 자연스럽게 드러난다.

## FinalPrice — 모든 것의 합류점

`FinalPrice` 메서드는 이 과제에서 만든 모든 요소를 한 곳에 모은다:
- `Get`을 호출해서 에러를 확인하고
- `PricingRule` interface를 통해 할인을 적용하고
- nil 체크로 규칙이 없는 경우도 처리한다

이 함수 하나에 struct, method, interface, error가 전부 등장한다. 입문자가 마지막에 이걸 읽으면 "아, 이것들이 이렇게 엮이는구나" 하는 감각을 얻게 된다.

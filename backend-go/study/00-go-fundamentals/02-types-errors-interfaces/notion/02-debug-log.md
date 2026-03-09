# 디버그 기록 — 어디서 막혔고 어떻게 풀었나

## pointer receiver vs value receiver 혼동

처음에 `Catalog`의 메서드를 전부 value receiver로 작성했다. `Add`를 호출해도 원본 map이 변경되지 않는 문제가 생겼다. Go에서 value receiver는 struct의 복사본 위에서 동작하기 때문이다.

```go
// 잘못된 버전: value receiver
func (c Catalog) Add(item Item) error {
    c.items[item.SKU] = item  // 복사본에만 추가됨
    return nil
}
```

`go test`를 돌리면 `Add` 후에 `Get`이 항상 "not found"를 반환했다. 원인을 찾는 데 시간이 걸렸는데, 에러 메시지가 무관한 것처럼 보였기 때문이다. 실제로는 Add가 아무 효과도 내지 못하고 있었다.

수정은 간단했다—`func (c *Catalog) Add(...)` 로 pointer receiver로 바꾸면 된다. 그런데 이걸 경험하지 않으면 "왜 pointer receiver를 쓰는지"를 몸으로 알기 어렵다.

## errors.As의 타입 매칭

`NotFoundError`를 검사할 때 처음에 이렇게 썼다:

```go
var notFound NotFoundError
if !errors.As(err, &notFound) { ... }
```

이건 맞는 코드다. 하지만 처음에 `errors.As(err, notFound)` 로 포인터 없이 호출했다가 컴파일 에러를 만났다. `errors.As`의 두 번째 인자는 반드시 포인터여야 한다—값을 채워 넣어야 하니까.

```
cannot use notFound (variable of type NotFoundError) as type *error in argument
```

Go의 에러 처리에서 `errors.Is`와 `errors.As`의 차이를 명확히 구분한 건 이 실수를 겪고 나서였다:
- `errors.Is`: 에러 값 자체를 비교 (sentinel error 용)
- `errors.As`: 에러를 특정 타입으로 변환 (custom error 타입 용)

## 할인율이 0이거나 음수일 때

`PercentageDiscount`에서 할인율이 0 이하일 때를 처리하지 않으면, 가격이 원래보다 올라가는 기이한 결과가 나올 수 있다. 예를 들어 `Percent: -10`이면 가격이 110%가 된다.

처음에는 이걸 테스트에서 잡지 않았다. 나중에 방어 코드를 넣었다:

```go
if d.Percent <= 0 {
    return priceCents
}
```

이건 "할인이 없다면 원래 가격을 반환"하는 단순한 로직이지만, 이런 경계 조건을 명시적으로 처리해 두는 습관은 이후 과제에서 계속 이어진다.

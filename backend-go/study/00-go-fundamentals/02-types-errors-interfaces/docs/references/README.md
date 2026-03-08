# References

## 1. Effective Go

- Title: Effective Go
- URL: https://go.dev/doc/effective_go
- Checked date: 2026-03-07
- Why: method, interface, receiver 선택 기준을 다시 확인했다.
- Learned: 인터페이스는 구현체가 아니라 호출 지점의 필요에 맞게 설계하는 편이 낫다.
- Effect: 할인 규칙만 인터페이스로 남기고 카탈로그 자체는 구체 타입으로 유지했다.

## 2. Errors Package

- Title: Package errors
- URL: https://pkg.go.dev/errors
- Checked date: 2026-03-07
- Why: `errors.Is`와 `errors.As` 사용법을 확인했다.
- Learned: sentinel error와 custom error를 같이 써도 테스트는 안정적으로 작성 가능하다.
- Effect: `ErrDuplicateSKU`와 `NotFoundError`를 분리했다.


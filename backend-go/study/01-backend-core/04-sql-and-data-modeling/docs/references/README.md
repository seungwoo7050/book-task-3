# References

## 1. SQLite Foreign Keys

- Title: SQLite Foreign Key Support
- URL: https://www.sqlite.org/foreignkeys.html
- Checked date: 2026-03-07
- Why: FK 제약이 이 과제의 모델링 목표와 잘 맞는지 확인했다.
- Learned: 입문 단계에서도 FK를 빼면 나중에 데이터 정합성 이해가 약해진다.
- Effect: `inventory`에 FK와 composite PK를 모두 뒀다.

## 2. `database/sql` Package

- Title: Package sql
- URL: https://pkg.go.dev/database/sql
- Checked date: 2026-03-07
- Why: transaction과 query loop의 기본 패턴을 확인했다.
- Learned: `QueryRowContext`, `BeginTx`, `ExecContext` 세 개만으로도 핵심 흐름을 보여줄 수 있다.
- Effect: 예제 코드를 repository abstraction 없이도 읽히는 수준으로 유지했다.


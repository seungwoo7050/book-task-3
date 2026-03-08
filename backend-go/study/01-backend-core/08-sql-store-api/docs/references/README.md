# References

## 1. Go Database Access

- Title: Executing SQL statements that don't return data
- URL: https://go.dev/doc/database/change-data
- Checked date: 2026-03-07
- Why: `ExecContext`, `RowsAffected`, transaction 패턴을 다시 확인했다.
- Learned: 작은 예제에서도 context-aware DB 호출 패턴을 먼저 익히는 편이 낫다.
- Effect: repository 메서드 전반에 `Context`를 유지했다.

## 2. SQLite UPSERT

- Title: SQLite UPSERT
- URL: https://www.sqlite.org/lang_upsert.html
- Checked date: 2026-03-07
- Why: 업데이트/삽입 흐름과 충돌 처리 방식을 비교했다.
- Learned: 이 과제에서는 충돌 감지를 version update로 분리하는 편이 의도가 더 잘 드러난다.
- Effect: create와 update를 별도 경로로 유지했다.


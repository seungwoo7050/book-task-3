# References

## 1. OWASP Authentication Cheat Sheet

- Title: Authentication Cheat Sheet
- URL: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- Checked date: 2026-03-07
- Why: access/refresh token과 인증 실패 응답의 기본 원칙을 다시 확인했다.
- Learned: 대표작도 토큰 발급보다 세션 회전과 만료 처리 규칙이 더 중요하다.
- Effect: refresh token rotation과 logout revoke를 기본 흐름으로 고정했다.

## 2. PostgreSQL `INSERT ... ON CONFLICT`

- Title: PostgreSQL Documentation - INSERT
- URL: https://www.postgresql.org/docs/current/sql-insert.html
- Checked date: 2026-03-07
- Why: notification dedupe와 seed idempotency 처리를 단순하게 만들기 위해 참고했다.
- Learned: worker 중복 처리는 앱 코드보다 unique constraint와 `ON CONFLICT DO NOTHING`이 더 안정적이다.
- Effect: notifications는 `(user_id, source_event_id)` unique로 보호했다.

## 3. Redis Go Client

- Title: redis/go-redis
- URL: https://github.com/redis/go-redis
- Checked date: 2026-03-07
- Why: dashboard cache와 refresh session 저장소 구현에 사용했다.
- Learned: 대표작에서는 캐시와 세션 저장소를 같은 Redis에 두더라도 key namespace를 분리하는 편이 읽기 쉽다.
- Effect: `workspace-saas:refresh:*`, `workspace-saas:dashboard:*` 키를 따로 썼다.

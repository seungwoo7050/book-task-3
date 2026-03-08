# Presentation Assets

이 폴더는 발표 자료에서 참조하는 실제 데모 캡처를 둔다.

## Current Capture Set

- [demo-2026-03-07](demo-2026-03-07)

## Regenerate

```bash
cd 05-portfolio-projects/18-workspace-saas-api/go
make demo-capture
```

Docker Desktop이 불안정하면, 이미 떠 있는 Postgres/Redis에 연결해서 아래처럼 직접 실행해도 된다.

```bash
cd 05-portfolio-projects/18-workspace-saas-api/go
DATABASE_URL='postgres://.../workspace_saas?sslmode=disable' REDIS_ADDR='localhost:6381' ./scripts/demo_capture.sh
```

현재 스크립트는 실제 요청으로 캡처를 만든 뒤, public docs에 남는 토큰 문자열만 마스킹한다.

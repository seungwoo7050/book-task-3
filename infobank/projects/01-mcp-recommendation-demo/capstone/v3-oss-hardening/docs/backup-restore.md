# 백업과 복구

## 데이터베이스 백업

Compose 기본 DB 이름은 `study1_v3`다.

```bash
pg_dump postgresql://postgres:postgres@127.0.0.1:5543/study1_v3 > study1-v3-backup.sql
```

## 데이터베이스 복구

```bash
psql postgresql://postgres:postgres@127.0.0.1:5543/study1_v3 < study1-v3-backup.sql
```

## 이식 가능한 카탈로그 스냅샷

DB dump 대신 catalog/eval/release candidate 상태만 옮기려면 bundle export를 쓴다.

1. 콘솔에서 `Export Bundle`
2. JSON 저장
3. 다른 인스턴스에서 `Import Bundle`

이 방식은 user/session/audit/job log를 옮기지 않고 운영 대상 데이터만 옮긴다.

# 02 WAL Recovery — Series Map

01에서 남긴 빈자리 — "flush 전에 죽으면 데이터는 어디로 가는가." 이 프로젝트가 그 답이다. WAL을 달아서 memtable보다 먼저 디스크에 기록을 남기고, crash 뒤에도 그 기록을 재생해서 상태를 복구한다. 핵심 질문은 "어디까지 재생하느냐"였다.

## 이 프로젝트가 답하는 질문

- append-before-apply 순서가 왜 durability의 전제 조건인가
- 손상된 레코드를 만났을 때 전부 건너뛸 것인가, 아니면 첫 불신 지점에서 멈출 것인가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md) — 바이너리 WAL 포맷과의 첫 만남
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md) — recovery는 어디서 멈추는가
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — flush가 WAL을 리셋하는 순간

## 참조한 실제 파일

- `python/database-internals/projects/02-wal-recovery/src/wal_recovery/store.py`
- `python/database-internals/projects/02-wal-recovery/tests/test_wal_recovery.py`
- `python/database-internals/projects/02-wal-recovery/src/wal_recovery/__main__.py`
- `python/database-internals/projects/02-wal-recovery/README.md`
- `python/database-internals/projects/02-wal-recovery/problem/README.md`
- `python/database-internals/projects/02-wal-recovery/pyproject.toml`

## 재검증 명령

```bash
cd python/database-internals/projects/02-wal-recovery
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m wal_recovery
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`

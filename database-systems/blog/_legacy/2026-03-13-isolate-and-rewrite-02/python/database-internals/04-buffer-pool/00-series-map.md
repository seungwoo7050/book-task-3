# 04 Buffer Pool — Series Map

disk-backed page를 메모리에 캐시하고 pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현합니다. 이 시리즈는 기존 초안의 말투를 따라가지 않고, 실제 코드와 검증 신호를 다시 읽으면서 판단이 어디서 바뀌는지에만 집중한다.

## 이 프로젝트가 답하는 질문

- page id로 file path와 page number를 안정적으로 분리해야 합니다.
- fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다.

## 작업 산출물

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md) — 파일 구조와 테스트 이름으로 범위를 다시 잡는 구간
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md) — 핵심 invariant를 코드 조각으로 고정하는 구간
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md) — 실제 pass 신호와 남은 경계를 정리하는 구간

## 참조한 실제 파일

- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`
- `database-systems/python/database-internals/projects/04-buffer-pool/tests/test_buffer_pool.py`
- `database-systems/python/database-internals/projects/04-buffer-pool/README.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/problem/README.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/docs/README.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/__main__.py`

## 재검증 명령

```bash
PYTHONPATH=src .venv/bin/python -m pytest
PYTHONPATH=src .venv/bin/python -m buffer_pool
```

## Git Anchor

- `2026-03-13 abeead6 docs: TRACK 1 에대한 blog/ 작업 1차 완료`
- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`

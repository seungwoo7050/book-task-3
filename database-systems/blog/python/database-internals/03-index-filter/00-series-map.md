# 03 Index Filter — Series Map

이 시리즈의 출발점은 단순하다. `get(key)`를 할 때 매번 SSTable 전체를 읽는 건 너무 비싸다. 그런데 "빠르게 찾기"보다 먼저 "없는 키를 빠르게 버리기"가 더 싸다는 사실을 Bloom filter가 보여 준다.

## 이 프로젝트가 답하는 질문

- Bloom filter는 어디까지 책임지고, 어디서 sparse index에게 바통을 넘기는가
- footer metadata를 파일 끝에 박아 두는 선택이 왜 lookup 비용과 직결되는가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-integration-and-tradeoffs.md](30-chronology-integration-and-tradeoffs.md)
4. [40-chronology-verification-and-boundaries.md](40-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/database-internals/projects/03-index-filter/src/index_filter/table.py`
- `python/database-internals/projects/03-index-filter/src/index_filter/__main__.py`
- `python/database-internals/projects/03-index-filter/tests/test_index_filter.py`
- `python/database-internals/projects/03-index-filter/README.md`
- `python/database-internals/projects/03-index-filter/problem/README.md`
- `python/database-internals/projects/03-index-filter/docs/concepts/bloom-filter-sizing.md`
- `python/database-internals/projects/03-index-filter/docs/concepts/sparse-index-scan.md`
- `python/database-internals/projects/03-index-filter/pyproject.toml`

## 재검증 명령

```bash
cd python/database-internals/projects/03-index-filter
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m index_filter
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`

# 03 Index Filter — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. Bloom filter와 sparse index를 SSTable에 결합하여 읽기 경로를 최적화하는 전체 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — 왜 index filter가 필요하고 어떻게 구현했는지 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`Bloom filter` · `sparse index` · `SSTable` · `false positive rate` · `block scan` · `double hashing` · `footer metadata` · `binary serialization` · `point lookup` · `bounded I/O`

## 프로젝트 위치

```
python/database-internals/03-index-filter/
├── src/index_filter/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   └── table.py         # BloomFilter, SparseIndex, SSTable, 직렬화
├── tests/
│   └── test_index_filter.py  # 4개 테스트 케이스
├── docs/concepts/
│   ├── bloom-filter-sizing.md
│   └── sparse-index-scan.md
└── problem/README.md
```

## 연관 프로젝트

- **Go 06-index-filter**: 동일 개념의 Go 구현. MurmurHash3 double hashing, magic "SIF1" footer.
- **Py 01-mini-lsm-store**: 이 프로젝트가 최적화하는 대상인 기본 SSTable/LSM 구조.
- **Py 02-wal-recovery**: 동일한 binary 직렬화 패턴(TOMBSTONE_MARKER, struct.pack)을 공유.

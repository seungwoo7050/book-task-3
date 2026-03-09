# 04 Buffer Pool — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. LRU 캐시와 buffer pool manager를 Python으로 구현하는 전체 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — 왜 buffer pool이 필요하고 어떻게 구현했는지 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`LRU cache` · `OrderedDict` · `buffer pool` · `page` · `pin count` · `dirty flag` · `eviction` · `write-back` · `page_id` · `fixed-size page`

## 프로젝트 위치

```
python/database-internals/04-buffer-pool/
├── src/buffer_pool/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   └── core.py          # LRUCache, Page, BufferPool, parse_page_id
├── tests/
│   └── test_buffer_pool.py  # 7개 테스트 케이스
├── docs/concepts/
│   ├── lru-eviction.md
│   └── pin-and-dirty.md
└── problem/README.md
```

## 연관 프로젝트

- **Go 07-buffer-pool**: 동일 개념의 Go 구현. HashMap+DoublyLinkedList로 직접 LRU 구현.
- **Py 03-index-filter**: SSTable 읽기 경로에서 buffer pool이 캐시 역할을 해야 하는 이유를 보여줌.
- **Py 05-mvcc**: buffer pool 위에 트랜잭션 관리가 올라가는 다음 단계.

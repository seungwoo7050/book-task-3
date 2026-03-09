# 05 MVCC — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. Python database-internals 트랙의 마지막 프로젝트로서, snapshot isolation 기반 MVCC 트랜잭션 관리의 전체 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — snapshot isolation과 version chain의 구현 이야기 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`MVCC` · `snapshot isolation` · `version chain` · `write-write conflict` · `first-committer-wins` · `transaction manager` · `write set` · `garbage collection` · `read-your-own-write` · `abort rollback`

## 프로젝트 위치

```
python/database-internals/05-mvcc/
├── src/mvcc_lab/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   └── core.py          # Version, VersionStore, Transaction, TransactionManager
├── tests/
│   └── test_mvcc.py     # 7개 테스트 케이스
├── docs/concepts/
│   ├── snapshot-visibility.md
│   └── write-conflict.md
└── problem/README.md
```

## 연관 프로젝트

- **Go 08-mvcc**: 동일 개념의 Go 구현. 삽입 정렬 기반 version chain, 동일한 first-committer-wins 정책.
- **Py 04-buffer-pool**: buffer pool 위에 MVCC가 올라가는 전체 아키텍처 맥락.
- **Py 01-mini-lsm-store**: MVCC가 관리하는 데이터의 최종 저장 계층.

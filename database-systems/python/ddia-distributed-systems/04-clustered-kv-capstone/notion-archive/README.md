# 04 Clustered KV Capstone — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. Python 분산 시스템 트랙의 최종 프로젝트로서, shard routing + leader-follower replication + disk-backed store + FastAPI를 하나로 통합하는 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — 세 개의 독립적 개념이 하나의 클러스터가 되는 과정 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`clustered KV` · `static topology` · `DiskStore` · `ReplicaGroup` · `ShardRing` · `Cluster` · `leader-follower` · `watermark sync` · `restart recovery` · `FastAPI` · `JSON Lines`

## 프로젝트 위치

```
python/ddia-distributed-systems/04-clustered-kv-capstone/
├── src/clustered_kv/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   ├── core.py          # DiskStore, ShardRing, Cluster, ReplicaGroup
│   └── app.py           # FastAPI 엔드포인트, create_app
├── tests/
│   └── test_clustered_kv.py  # 4개 테스트 케이스
└── problem/README.md
```

## 연관 프로젝트

- **Go DDIA-05 (clustered-kv-capstone)**: 동일 개념의 Go 구현. Raft 합의 포함, FastAPI 대신 Go 내장 서버.
- **Py DDIA-02 (leader-follower-replication)**: 이 프로젝트에 통합된 복제 로직의 원본.
- **Py DDIA-03 (shard-routing)**: 이 프로젝트에 통합된 라우팅 로직의 원본.
- **Py DB-01 (mini-lsm-store)**: DiskStore의 JSON Lines 패턴 원본.

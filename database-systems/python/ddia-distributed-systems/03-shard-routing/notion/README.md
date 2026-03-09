# 03 Shard Routing — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. Consistent hash ring과 virtual node를 사용하여 키를 노드에 균등 분배하고, 노드 변경 시 최소한의 키만 재배치하는 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — consistent hashing이 해결하는 문제와 구현 과정 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`consistent hashing` · `hash ring` · `virtual node` · `bisect` · `shard routing` · `rebalance` · `moved keys` · `batch routing` · `SHA-256`

## 프로젝트 위치

```
python/ddia-distributed-systems/03-shard-routing/
├── src/shard_routing/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   └── core.py          # hash_value, RingEntry, Ring, Router
├── tests/
│   └── test_shard_routing.py  # 3개 테스트 케이스
└── problem/README.md
```

## 연관 프로젝트

- **Go DDIA-03 (shard-routing)**: 동일 개념의 Go 구현. MurmurHash3 사용, shared/hash 의존.
- **Py DDIA-02 (leader-follower-replication)**: 샤드 내의 복제 메커니즘.
- **Py DDIA-04 (clustered-kv-capstone)**: 최종 통합에서 shard 라우팅을 키 분배에 사용.

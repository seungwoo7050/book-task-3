# 02 Leader-Follower Replication — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. Leader-follower 복제 모델에서 append-only log와 watermark 기반 동기화를 구현하는 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — 왜 복제가 필요하고 어떻게 동기화하는지 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`leader-follower` · `append-only log` · `replication log` · `watermark` · `incremental sync` · `idempotent apply` · `replicate_once` · `offset` · `mutation log`

## 프로젝트 위치

```
python/ddia-distributed-systems/02-leader-follower-replication/
├── src/leader_follower/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   └── core.py          # LogEntry, ReplicationLog, Leader, Follower, replicate_once
├── tests/
│   └── test_replication.py  # 3개 테스트 케이스
└── problem/README.md
```

## 연관 프로젝트

- **Go DDIA-02 (leader-follower-replication)**: 동일 개념의 Go 구현. `*string`으로 optional value 처리.
- **Py DDIA-01 (rpc-framing)**: 네트워크 계층. 실제 분산 시스템에서는 RPC 위에 복제가 올라감.
- **Py DDIA-04 (clustered-kv-capstone)**: 최종 통합에서 복제 메커니즘으로 사용.

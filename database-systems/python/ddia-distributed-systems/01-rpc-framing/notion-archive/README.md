# 01 RPC Framing — Notion 문서 가이드

## 이 폴더의 목적

소스코드만으로는 알 수 없는 **설계 동기, 의사결정 과정, 개발 타임라인**을 기록한다. Python 분산 시스템 트랙의 첫 프로젝트로서, TCP 위에 length-prefixed framing과 correlation ID 기반 RPC를 구현하는 과정을 담는다.

## 문서 안내

| 문서 | 설명 | 이런 경우에 읽으세요 |
|------|------|---------------------|
| [essay.md](essay.md) | 블로그 스타일 에세이 — TCP 바이트 스트림 위에 메시지 경계를 복원하고 RPC를 올리는 이유 | 프로젝트의 맥락과 설계 철학을 이해하고 싶을 때 |
| [timeline.md](timeline.md) | 개발 과정 타임라인 — CLI 명령어, 패키지 설치, 구현 순서 | 이 프로젝트를 처음부터 재현하고 싶을 때 |

## 키워드

`TCP framing` · `length prefix` · `FrameDecoder` · `correlation ID` · `pending map` · `RPCServer` · `RPCClient` · `concurrent calls` · `timeout` · `threading`

## 프로젝트 위치

```
python/ddia-distributed-systems/01-rpc-framing/
├── src/rpc_framing/
│   ├── __init__.py      # public exports
│   ├── __main__.py      # demo 엔트리포인트
│   └── core.py          # encode_frame, FrameDecoder, RPCServer, RPCClient
├── tests/
│   └── test_rpc_framing.py  # 5개 테스트 케이스
├── docs/concepts/
│   ├── frame-boundary.md
│   └── pending-map.md
└── problem/README.md
```

## 연관 프로젝트

- **Go DDIA-01 (rpc-framing)**: 동일 개념의 Go 구현. goroutine + channel 기반.
- **Py DDIA-02 (leader-follower-replication)**: 이 RPC 계층 위에 복제 프로토콜이 올라감.
- **Py DDIA-04 (clustered-kv-capstone)**: 최종 통합 프로젝트에서 RPC를 네트워크 계층으로 사용.

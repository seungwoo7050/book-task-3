# DB Study Archive

이 저장소는 데이터베이스 내부와 분산 시스템을 함께 배우는 학습 아카이브다. 공개 루트는 언어 기준으로 나뉜다.

## Public Roots

- [go/README.md](go/README.md): 전체 커리큘럼을 다루는 정본 슈퍼셋
- [python/README.md](python/README.md): 낮은 진입장벽을 위한 입문 트랙
- [docs/README.md](docs/README.md): 커리큘럼 감사, 언어별 규칙, 레거시 대응표, 교차 매핑
- `legacy/`: 존재하는 경우 읽기 전용 참고 자료

## Recommended Path

1. Python으로 저장 엔진과 분산 시스템의 핵심 흐름을 먼저 잡는다.
2. Go로 전체 커리큘럼과 심화 분산 주제를 따라간다.

## Current State

- Go는 `database-internals` `01-08`, `ddia-distributed-systems` `01-05`를 모두 제공한다.
- Python은 입문 경로로 재구성한 9개 프로젝트를 제공한다.
- 각 프로젝트는 자기 디렉터리에서 독립적으로 설치, 테스트, 데모 실행한다.

## Verified Starting Points

```bash
cd python/database-internals/01-mini-lsm-store
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m mini_lsm_store

cd go/database-internals/01-memtable-skiplist
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```

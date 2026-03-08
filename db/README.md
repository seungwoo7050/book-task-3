# DB Study Archive

이 저장소는 데이터 시스템 학습용 아카이브다. `legacy/`는 기존 Node.js 기반 실습 트리를 보존하는 참조 영역이고, `study/`는 새 정본 학습 트리다.

## 현재 정본 표면

- [docs/README.md](docs/README.md): 커리큘럼 감사, 레거시 매핑, 마이그레이션 규칙
- [study/database-internals/README.md](study/database-internals/README.md): 단일 노드 저장 엔진 트랙
- [study/ddia-distributed-systems/README.md](study/ddia-distributed-systems/README.md): 분산 시스템 트랙
- `legacy/`: 읽기 전용 참고 자료

## 학습 트랙

### Database Internals

1. `01-memtable-skiplist`
2. `02-sstable-format`
3. `03-mini-lsm-store`
4. `04-wal-recovery`
5. `05-leveled-compaction`
6. `06-index-filter`
7. `07-buffer-pool`
8. `08-mvcc`

### DDIA Distributed Systems

1. `01-rpc-framing`
2. `02-leader-follower-replication`
3. `03-shard-routing`
4. `04-raft-lite`
5. `05-clustered-kv-capstone`

## 실행 정책

- 루트 빌드 인터페이스는 제공하지 않는다.
- 각 프로젝트는 자기 디렉터리에서 독립적으로 빌드하고 테스트한다.
- `legacy/package.json`의 루트 스크립트 일부는 실제 파일과 어긋나므로 새 정본 문서에서는 사용하지 않는다.

## 검증된 시작점

```bash
cd study/database-internals/01-memtable-skiplist/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```

## 현재 상태

- `study/`의 13개 프로젝트가 모두 `verified` 상태다.
- 각 프로젝트는 `problem/`, `go/`, `docs/` 공개 표면과 로컬 전용 `notion/` 노트를 갖는다.
- 검증은 루트 monorepo 명령이 아니라 프로젝트 로컬 `GOWORK=off go test ./...` 및 데모 실행 기준으로 한다.

## 언어 선택

- 정식 구현 언어: Go 1.26.0
- 프레임워크: 없음
- 기본 원칙: 표준 라이브러리 우선, 프로젝트별 국소 검증

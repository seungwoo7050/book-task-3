# 08 MVCC

snapshot isolation을 위한 version chain과 transaction manager를 구현합니다.

## 이 프로젝트에서 배우는 것

- snapshot timestamp가 어떤 version을 볼 수 있는지 판단하는 규칙을 익힙니다.
- first-committer-wins 충돌 판정을 이해합니다.
- stale version GC가 왜 필요한지 확인합니다.

## 먼저 알고 있으면 좋은 것

- 기본적인 transaction, commit, abort 개념을 알고 있으면 좋습니다.
- 단일 key-value store 위에서 version chain을 관리하는 감각이 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `internal/`와 `tests/`를 함께 읽고, 마지막에 `cmd/mvcc/`로 동작 예시를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/mvcc/`, `tests/`, `cmd/mvcc/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/database-internals/08-mvcc
GOWORK=off go test ./...
GOWORK=off go run ./cmd/mvcc
```

## 구현에서 집중할 포인트

- read-your-own-write와 snapshot visibility가 동시에 만족되는지 확인합니다.
- 충돌 판정이 commit 시점에 일관적으로 수행되는지 봅니다.
- abort cleanup과 stale version GC가 테스트에서 드러나는지 확인합니다.

## 포트폴리오로 발전시키려면

- lock manager, transaction state visualizer, long-running read 시나리오를 추가하면 깊이가 생깁니다.
- 격리 수준 비교 실험을 문서화하면 학습 레포에서 포트폴리오 레포로 옮기기 좋습니다.

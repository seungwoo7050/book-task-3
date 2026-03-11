# 문제 프레이밍

## 왜 이 프로젝트를 하는가
한 key의 최신 값 하나만 보는 대신 version chain과 snapshot visibility를 도입해 transaction isolation을 설명하는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Go
- 이전 단계: 07 Buffer Pool
- 다음 단계: 이 트랙의 마지막 프로젝트
- 지금 답하려는 질문: 같은 key에 대해 여러 transaction이 겹칠 때, 누가 어떤 version을 볼 수 있고 어떤 commit은 거절되어야 하는가?

## 이번 구현에서 성공으로 보는 것
- 기본 read/write가 version chain 위에서 동작해야 합니다.
- transaction 시작 시점의 snapshot 기준으로 visible version이 선택되어야 합니다.
- read-your-own-write가 보장되어야 합니다.
- 같은 key를 쓰는 transaction 사이에 first-committer-wins 충돌 검사가 있어야 합니다.
- abort cleanup과 stale version GC가 동작해야 합니다.

## 먼저 열어 둘 파일
- `../internal/mvcc/mvcc.go`: `VersionStore`, `TransactionManager`, commit/abort/GC 로직이 모두 모여 있습니다.
- `../tests/mvcc_test.go`: snapshot isolation, conflict, abort, GC가 어디서 깨지는지 바로 보여 줍니다.
- `../cmd/mvcc/main.go`: 동시 transaction에서 오래된 snapshot이 어떤 값을 보는지 간단히 보여 주는 데모입니다.
- `../docs/concepts/snapshot-visibility.md`: 어떤 version이 읽혀야 하는지 기준을 먼저 맞출 때 도움이 됩니다.

## 의도적으로 남겨 둔 범위 밖 항목
- predicate read, phantom 방지, lock manager는 다루지 않습니다.
- range index와 storage engine 통합은 아직 없는 학습용 memory model입니다.

## 데모에서 바로 확인할 장면
- concurrent transaction에서 `t2`가 어떤 값을 보는지 출력합니다.

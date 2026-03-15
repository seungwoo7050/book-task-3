# 13-distributed-log-core-go 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 length-prefixed record store를 구현한다, offset -> position을 매핑하는 fixed-width mmap index를 구현한다, segment가 base offset과 next offset을 관리하며 full 상태를 판정한다를 한 흐름으로 설명하고 검증한다. 핵심은 `newIndex`와 `Write`, `Read` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- length-prefixed record store를 구현한다.
- offset -> position을 매핑하는 fixed-width mmap index를 구현한다.
- segment가 base offset과 next offset을 관리하며 full 상태를 판정한다.
- 첫 진입점은 `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/errors.go`이고, 여기서 `newIndex`와 `Write` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/errors.go`: 핵심 구현을 담는 파일이다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/index.go`: `newIndex`, `Write`, `Read`, `Entries`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/log.go`: `NewLog`, `setup`, `newSegment`, `Append`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/segment.go`: `newSegment`, `Append`, `Read`, `IsFull`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/store.go`: `newStore`, `Append`, `Read`, `ReadAt`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/index_test.go`: `TestIndexWriteRead`, `TestIndexReadEmpty`, `TestIndexFull`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/log_test.go`: `TestLogAppendRead`, `TestLogMultipleSegments`, `TestLogRestore`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/segment_test.go`: `TestSegmentAppendRead`, `TestSegmentReopen`, `TestSegmentFull`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/errors.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestIndexWriteRead` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core/problem test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestIndexWriteRead`와 `TestIndexReadEmpty`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/errors.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/index.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/log.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/segment.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/store.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/index_test.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/log_test.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/segment_test.go`
- `../study/02-distributed-systems/13-distributed-log-core/problem/Makefile`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/go.mod`

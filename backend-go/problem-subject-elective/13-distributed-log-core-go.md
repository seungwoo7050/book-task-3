# 13-distributed-log-core-go 문제지

## 왜 중요한가

append-only distributed commit log의 핵심인 store, index, segment, log abstraction을 구현한다.

## 목표

시작 위치의 구현을 완성해 length-prefixed record store를 구현한다, offset -> position을 매핑하는 fixed-width mmap index를 구현한다, segment가 base offset과 next offset을 관리하며 full 상태를 판정한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/errors.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/index.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/log.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/segment.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/index_test.go`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/log_test.go`
- `../study/02-distributed-systems/13-distributed-log-core/problem/Makefile`
- `../study/02-distributed-systems/13-distributed-log-core/solution/go/go.mod`

## starter code / 입력 계약

- `../study/02-distributed-systems/13-distributed-log-core/solution/go/log/errors.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- length-prefixed record store를 구현한다.
- offset -> position을 매핑하는 fixed-width mmap index를 구현한다.
- segment가 base offset과 next offset을 관리하며 full 상태를 판정한다.
- log가 active segment rotation과 read/append/reset을 지원한다.
- 파일 정리와 reopen 시나리오를 테스트로 검증한다.

## 제외 범위

- replication layer
- networked consensus
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `newIndex`와 `Write`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestIndexWriteRead`와 `TestIndexReadEmpty`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/13-distributed-log-core/problem test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`13-distributed-log-core-go_answer.md`](13-distributed-log-core-go_answer.md)에서 확인한다.

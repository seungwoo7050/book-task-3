# quorum-and-consistency 문제지

## 왜 중요한가

replica 3개를 가진 versioned register를 구현해야 합니다. N/W/R 정책에 따라 write quorum과 read quorum을 검증해야 합니다. write는 quorum이 확보될 때만 version을 올려야 합니다. read는 responder 집합 안에서 가장 높은 version을 골라 반환해야 합니다.

## 목표

시작 위치의 구현을 완성해 replica 3개를 가진 versioned register를 구현해야 합니다, N/W/R 정책에 따라 write quorum과 read quorum을 검증해야 합니다, write는 quorum이 확보될 때만 version을 올려야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/ddia-distributed-systems/projects/06-quorum-and-consistency/cmd/quorum-demo/main.go`
- `../go/ddia-distributed-systems/projects/06-quorum-and-consistency/internal/quorum/quorum.go`
- `../go/ddia-distributed-systems/projects/06-quorum-and-consistency/tests/quorum_test.go`

## starter code / 입력 계약

- `../go/ddia-distributed-systems/projects/06-quorum-and-consistency/cmd/quorum-demo/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- replica 3개를 가진 versioned register를 구현해야 합니다.
- N/W/R 정책에 따라 write quorum과 read quorum을 검증해야 합니다.
- write는 quorum이 확보될 때만 version을 올려야 합니다.
- read는 responder 집합 안에서 가장 높은 version을 골라 반환해야 합니다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `mustCluster`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestReadReturnsLatestWhenQuorumsOverlap`와 `TestStaleReadAppearsWhenQuorumsDoNotOverlap`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/06-quorum-and-consistency && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`quorum-and-consistency_answer.md`](quorum-and-consistency_answer.md)에서 확인한다.

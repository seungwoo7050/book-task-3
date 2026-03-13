# 13 Distributed Log Core 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../02-distributed-systems/13-distributed-log-core/README.md), [`problem/README.md`](../../02-distributed-systems/13-distributed-log-core/problem/README.md)
- 구현 표면:
- `solution/go/log/store.go`
- `solution/go/log/log.go`
- `solution/go/log/log_test.go`
- 검증 표면: `cd solution/go && go test -run TestLogRestore -v ./log`, `cd solution/go && go test ./log/... -bench=.`
- 개념 축: `store는 레코드 바이트를 순차 append하는 역할이다.`, `index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다.`, `segment는 store와 index를 묶은 관리 단위다.`

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

store, index, segment를 쌓아 append-only log가 reopen, segment split, truncate까지 버티게 만든다.

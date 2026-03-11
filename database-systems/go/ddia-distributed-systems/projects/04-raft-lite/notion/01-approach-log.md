# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### state transition을 `Node` 안에 명시적으로 둔다
- 관련 파일: `../internal/raft/raft.go`
- 판단: Follower, Candidate, Leader 전환이 한 파일 안에서 명확히 보이게 만들어 term 기반 reasoning을 쉽게 했습니다.

### leader authority와 commit rule을 한 흐름으로 묶는다
- 관련 파일: `../internal/raft/raft.go`
- 판단: 리더 선출만 있고 commit 기준이 없으면 consensus 설명이 반쪽이므로, replicated log와 commit index 계산을 함께 남겼습니다.

### higher term 수신 시 즉시 step down한다
- 관련 파일: `../internal/raft/raft.go`, `../tests/raft_test.go`
- 판단: 권한 갱신 규칙을 느슨하게 두면 split-brain 같은 오해가 커지므로, 더 높은 term을 보면 바로 follower로 내려오게 했습니다.

## 검증 명령
```bash
cd go/ddia-distributed-systems/projects/04-raft-lite
go test ./...
go run ./cmd/raft-lite
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- `leader=<id> commit=<n>` 출력은 election과 commit이 둘 다 작동한다는 최소 증거가 됩니다.
- leader-follower replication에서 consensus 단계로 넘어가며 무엇이 추가되었는지 비교 설명하기 좋습니다.
- step-down 규칙은 작지만 분산 시스템 감각을 보여 주는 강한 장면입니다.

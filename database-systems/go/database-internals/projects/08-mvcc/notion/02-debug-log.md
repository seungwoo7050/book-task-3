# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. snapshot이 future commit을 읽어 버리는 경우
- 의심 파일: `../internal/mvcc/mvcc.go`
- 깨지는 징후: transaction 시작 뒤에 생긴 commit이 바로 보이면 snapshot isolation이 무너집니다.
- 확인 테스트: `TestSnapshotIsolation`
- 다시 볼 질문: visible version 선택이 transaction의 snapshot 값보다 작은 committed version만 고르는가?

### 2. 동일 key write conflict를 놓치는 경우
- 의심 파일: `../internal/mvcc/mvcc.go`
- 깨지는 징후: 두 writer가 같은 key를 모두 commit하면 lost update가 발생합니다.
- 확인 테스트: `TestWriteWriteConflict`
- 다시 볼 질문: commit 시 자신의 snapshot 이후에 같은 key를 commit한 transaction을 검사하는가?

### 3. abort나 GC 뒤에 stale version이 남는 경우
- 의심 파일: `../internal/mvcc/mvcc.go`
- 깨지는 징후: abort된 쓰기가 보이거나 오래된 version chain이 끝없이 남으면 cleanup 경계가 잘못된 것입니다.
- 확인 테스트: `TestAbortAndDelete`, `TestGC`
- 다시 볼 질문: abort 시 자신의 version을 제거하고, GC는 가장 오래된 active snapshot보다 오래된 version만 지우는가?

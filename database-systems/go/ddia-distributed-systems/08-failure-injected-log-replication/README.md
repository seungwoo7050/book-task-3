# 08 Failure-Injected Log Replication

drop, duplicate, pause가 들어가는 작은 네트워크 하네스 위에서 append/ack 로그 복제와 quorum commit, follower catch-up을 재현합니다.

## 이 프로젝트에서 배우는 것

- dropped append가 retry로 수렴하는 흐름을 익힙니다.
- duplicate delivery가 follower 상태를 두 번 바꾸면 안 된다는 점을 확인합니다.
- follower 하나가 멈춰도 quorum commit은 유지되지만, 복구 전까지 lag는 남는다는 사실을 봅니다.

## 먼저 알고 있으면 좋은 것

- heartbeat와 leader election을 먼저 읽었으면 authority와 replication을 구분해서 보기 쉽습니다.
- full Raft가 아니라 single-leader append/ack replication이라는 점을 알고 시작하면 좋습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어 failure injection과 quorum commit 질문을 맞춥니다.
3. `internal/replication/`와 `tests/`를 함께 읽고, 마지막에 `cmd/failure-replication/`로 convergence 데모를 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `internal/replication/`, `tests/`, `cmd/failure-replication/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd go/ddia-distributed-systems/08-failure-injected-log-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/failure-replication
```

## 구현에서 집중할 포인트

- leader는 follower별 `nextIndex`를 유지해 drop 뒤에도 같은 entry를 다시 보내야 합니다.
- duplicate append는 log length와 applied count를 증가시키면 안 됩니다.
- commit index는 leader 자신과 follower ack 수를 기준으로만 올라가야 합니다.

## 포트폴리오로 발전시키려면

- ack drop, out-of-order delivery, backoff 정책을 추가하면 더 현실적인 replication harness가 됩니다.
- timeline trace와 metrics를 붙이면 장애 재현 포트폴리오로 확장하기 좋습니다.

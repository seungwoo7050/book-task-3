# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### append-only log에 연속 offset을 부여한다
- 관련 파일: `../internal/replication/replication.go`
- 판단: state의 진실은 current map이 아니라 mutation log라는 관점을 분명히 하기 위해 sequential offset을 기준으로 잡았습니다.

### follower는 watermark 이전 entry를 건너뛴다
- 관련 파일: `../internal/replication/replication.go`
- 판단: 재전송이 생겨도 상태가 뒤틀리지 않도록 `lastAppliedOffset` 또는 동등한 watermark를 유지합니다.

### delete도 같은 log shipping 경로를 탄다
- 관련 파일: `../internal/replication/replication.go`
- 판단: 삭제만 별도 제어 흐름으로 빼지 않고 mutation log의 한 종류로 취급해야 replication이 단순해집니다.

## 검증 명령
```bash
cd go/ddia-distributed-systems/projects/02-leader-follower-replication
go test ./...
go run ./cmd/replication
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- follower watermark 하나로 incremental sync와 idempotence를 동시에 설명할 수 있습니다.
- delete까지 같은 mutation log 경로를 탄다는 점은 replication 설계를 단순하게 만든 핵심입니다.
- 이 단계는 consensus 전 replication의 최소 모델이라는 점이 커리큘럼상 위치를 설명하기 좋습니다.

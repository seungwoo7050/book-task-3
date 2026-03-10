# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### consistent hash ring을 routing 계층으로 독립시킨다
- 관련 파일: `../internal/routing/routing.go`
- 판단: replication이나 consensus 이전에 key placement 문제를 따로 떼어 보려는 선택입니다.

### virtual node를 적극적으로 사용한다
- 관련 파일: `../internal/routing/routing.go`
- 판단: 실노드 수가 적어도 분산이 어느 정도 고르게 나오게 하려면 virtual node가 필요합니다.

### rebalance를 “얼마나 많이 움직였는가”로 본다
- 관련 파일: `../tests/routing_test.go`
- 판단: hash 값만 보는 대신, 노드 변경 후 실제 key 이동량을 테스트에서 확인하게 했습니다.

## 검증 명령
```bash
cd go/ddia-distributed-systems/03-shard-routing
go test ./...
go run ./cmd/shard-routing
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- 키 몇 개가 어떤 노드로 가는지 바로 보여 주는 데모는 routing 계층 설명에 매우 효과적입니다.
- consistent hashing과 virtual node를 분리해 설명하면 “왜 전체 재배치를 피할 수 있는가”가 전달됩니다.
- 해시 함수 선택보다 ring과 virtual node 구조가 더 본질적이라는 점을 강조할 수 있습니다.

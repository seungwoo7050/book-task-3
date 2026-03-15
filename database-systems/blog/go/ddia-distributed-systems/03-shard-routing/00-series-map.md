# 03 Shard Routing

## 이 랩의 실제 초점

이 프로젝트는 sharding을 "key를 어느 노드로 보낼까" 수준보다 더 구체적으로 다룬다. virtual node를 가진 consistent hash ring으로 deterministic placement를 만들고, membership 변화 뒤 얼마나 적은 key만 다시 이동하는지를 숫자로 확인한다. batch routing은 같은 node로 갈 key를 한 번에 묶는 표면을 제공한다.

즉 이 랩의 핵심은 control plane이 아니라 placement function과 rebalance accounting이다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/problem/README.md), [`routing.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go), [`routing_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/tests/routing_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/cmd/shard-routing/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- virtual node는 왜 필요한가
- ring lookup은 wrap-around를 어떻게 처리하는가
- membership 추가/제거 뒤 moved key 수는 어떻게 계산되는가
- batch routing은 왜 node별 key 묶음 shape를 돌려주는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/03-shard-routing/10-chronology-scope-and-surface.md): 문제 범위, ring/router 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/03-shard-routing/20-chronology-core-invariants.md): Murmur hash placement, virtual node insertion, wrap-around lookup, moved-key accounting을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/03-shard-routing/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/03-shard-routing/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/ddia-distributed-systems/03-shard-routing/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 분산 시스템 트랙에서 "key distribution과 rebalance cost를 정적으로 계산하는 단계"를 보여 준다. gossip, membership epoch, actual data relocation은 아직 없다. 대신 virtual node 기반 distribution, wrap-around lookup, moved-key accounting은 분명하게 드러난다.

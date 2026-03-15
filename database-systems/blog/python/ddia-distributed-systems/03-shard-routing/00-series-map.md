# 03 Shard Routing

## 이 랩의 실제 초점

겉으로는 "consistent hash ring을 구현한다"는 과제지만, 소스와 테스트를 다시 읽으면 더 정확한 초점은 두 가지다. 첫째, virtual node를 통해 key 분산이 한 노드에 과도하게 쏠리지 않게 만들 수 있는가. 둘째, membership이 바뀌었을 때 얼마나 적은 key만 다시 배치되는지를 숫자로 설명할 수 있는가.

이번 시리즈는 기존 blog를 근거로 삼지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/problem/README.md), [`core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py), [`test_shard_routing.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/tests/test_shard_routing.py), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- ring 위의 placement는 어떤 해시 규칙으로 결정되는가
- virtual node 수가 분산도에 어떤 영향을 주는가
- membership 변화 후 moved key 수는 어떻게 계산하는가
- 이 구현이 아직 다루지 않는 운영 문제는 무엇인가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/03-shard-routing/10-chronology-scope-and-surface.md): 문제 범위와 ring/router 표면을 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/03-shard-routing/20-chronology-core-invariants.md): hash ordering, wrap-around lookup, virtual node, moved key accounting을 소스 기준으로 설명한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/03-shard-routing/30-chronology-verification-and-boundaries.md): pytest와 수동 distribution 측정 결과를 바탕으로 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/03-shard-routing/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 기록한다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/python/ddia-distributed-systems/03-shard-routing/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 남긴다.

## 지금 기준의 결론

이 랩은 shard movement 자체를 실행하지 않는다. 대신 "어떤 노드가 key를 맡아야 하는지"와 "membership이 바뀌면 몇 개가 이동하는지"를 deterministic하게 계산하는 routing layer를 작게 구현한다. 그래서 gossip, membership epoch, actual data migration은 일부러 밖에 둔다.

한 번 더 정확히 말하면, 여기서 검증되는 것은 placement와 reassignment accounting이다. duplicate add/remove의 idempotence 같은 성질은 source에서 분명히 읽히지만, canonical pytest가 직접 잠그는 대표 보장은 아니다. distribution도 엄밀한 균등성 증명이 아니라 3000-key 샘플에서 `0.2 < share < 0.5`를 넘지 않는지 확인하는 수준으로 읽는 편이 맞다.

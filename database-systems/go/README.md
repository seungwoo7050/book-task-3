# Go Track

Go 트랙은 이 레포의 정본(superset)입니다. 저장 엔진과 분산 시스템을 더 세분화된 단계로 나눠 보기 때문에, “개념을 놓치지 않고 끝까지 따라가고 싶다”는 학습자에게 가장 적합합니다.

## 이 트랙이 잘 맞는 사람

- 자료구조, 파일 포맷, 오케스트레이션을 분리해서 보고 싶은 사람
- compaction, Raft-lite, quorum consistency, failure handling 같은 심화 슬롯까지 포함한 전체 경로를 보고 싶은 사람
- 나중에 공개용 포트폴리오를 더 시스템 지향적으로 확장하고 싶은 사람

## 포함 트랙

| 트랙 | 시작점 | 특징 |
| --- | --- | --- |
| [database-internals/README.md](database-internals/README.md) | `01-memtable-skiplist` | 자료구조부터 MVCC까지 저장 엔진 흐름을 세밀하게 나눠 봅니다. |
| [ddia-distributed-systems/README.md](ddia-distributed-systems/README.md) | `01-rpc-framing` | RPC부터 Raft-lite, clustered KV capstone을 거쳐 quorum, election, failure-injected replication까지 포함합니다. |
| [shared/README.md](shared/README.md) | `go/shared` | 여러 프로젝트가 재사용하는 공용 utility를 정리합니다. |

## 읽는 방법

1. 저장 엔진을 먼저 읽고, 분산 트랙으로 넘어가면 capstone이 더 잘 보입니다.
2. 각 프로젝트에서는 `problem → docs → implementation → notion` 순서를 유지하세요.
3. Python 트랙을 먼저 끝냈다면 [docs/language-crosswalk.md](../docs/language-crosswalk.md)를 함께 열어 두면 비교가 쉬워집니다.

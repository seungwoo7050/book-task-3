# Python Track

Python 트랙은 더 적은 프로젝트 수로 저장 엔진과 분산 시스템의 핵심 흐름을 먼저 익히도록 만든 입문 경로입니다. 구현 수를 줄인 대신, 각 프로젝트가 self-contained하게 이해되도록 문서와 읽는 순서를 더 친절하게 설명합니다.

## 이 트랙이 잘 맞는 사람

- 저장 엔진과 분산 시스템을 처음 함께 배우는 사람
- 빠르게 전체 그림을 잡고 나중에 Go 트랙으로 내려가고 싶은 사람
- 학습 레포를 바탕으로 자신의 포트폴리오 레포 구조를 먼저 잡고 싶은 사람

## 포함 트랙

| 트랙 | 시작점 | 특징 |
| --- | --- | --- |
| [database-internals/README.md](database-internals/README.md) | `01-mini-lsm-store` | memtable·SSTable·LSM을 한 프로젝트로 접어 더 빨리 큰 흐름을 봅니다. |
| [ddia-distributed-systems/README.md](ddia-distributed-systems/README.md) | `01-rpc-framing` | Raft를 제외하고, clustered KV capstone까지 이어지는 입문 분산 경로를 제공합니다. 이후 quorum, election, failure handling은 Go 심화 슬롯으로 넘어갑니다. |

## 읽는 방법

1. Python 트랙으로 큰 흐름을 먼저 잡습니다.
2. 더 세분화된 구현이나 심화 주제가 필요해지면 Go 트랙의 대응 프로젝트로 이동합니다.
3. 각 프로젝트 README 마지막의 “포트폴리오로 발전시키려면” 섹션을 보고, 무엇을 스스로 확장할지 정리해 보세요.

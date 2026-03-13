# Python Track

Python 쪽은 입문 경로입니다. 프로젝트 수를 줄이는 대신 각 프로젝트의 문제와 해법을 self-contained하게 따라갈 수 있게 구성했습니다.

## 누가 여기서 시작해야 하는가

- 저장 엔진과 분산 시스템의 큰 흐름을 먼저 잡고 싶은 사람에게 맞습니다.
- Go 심화 트랙으로 내려가기 전에 문제와 해법을 self-contained하게 따라가고 싶은 사람에게 맞습니다.
- 시작점은 [저장 엔진 입문 경로](database-internals/README.md)와 [분산 시스템 입문 경로](ddia-distributed-systems/README.md)입니다.

## 무엇이 들어 있는가

- [Database Internals](database-internals/README.md): 01~05까지 LSM, WAL, index/filter, buffer pool, MVCC를 다룹니다.
- [DDIA Distributed Systems](ddia-distributed-systems/README.md): 01~04까지 RPC, replication, routing, clustered KV capstone을 다룹니다.
- [Python Blog Index](../blog/python/README.md): Python 9개 프로젝트를 `src/tests` 중심의 source-first chronology로 다시 읽는 입구입니다.

## 읽는 순서

- 먼저 [docs/catalog/project-catalog.md](../docs/catalog/project-catalog.md)에서 전체 문제와 검증 명령을 훑습니다.
- 그다음 원하는 트랙 README로 내려가 프로젝트 표를 읽고, 각 프로젝트 README 첫 화면의 `문제 / 내 해법 / 검증`을 확인합니다.
- 세부 판단이 필요할 때만 `docs/`와 `notion/`으로 내려갑니다.
- 소스 기준 재구성 흐름이 필요할 때는 [../blog/python/README.md](../blog/python/README.md)에서 같은 프로젝트를 chronology로 따라갑니다.

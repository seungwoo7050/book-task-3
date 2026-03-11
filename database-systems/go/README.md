# Go Track

Go 쪽은 이 레포의 정본(superset)입니다. 프로젝트를 더 잘게 쪼개 두어 설계 질문과 구현 경계를 단계별로 추적하기 좋습니다.

## 누가 여기서 시작해야 하는가

- Python 입문 경로를 끝내고 같은 주제를 더 작은 설계 질문으로 다시 쪼개 읽고 싶은 사람에게 맞습니다.
- 자료구조, 파일 포맷, recovery, consensus-lite 같은 내부 경계를 직접 따라가고 싶은 사람에게 맞습니다.
- 시작점은 [저장 엔진 정본 경로](database-internals/README.md)와 [분산 시스템 심화 경로](ddia-distributed-systems/README.md)입니다.

## 무엇이 들어 있는가

- [Database Internals](database-internals/README.md): 01~08까지 자료구조, 포맷, recovery, compaction, cache, MVCC를 다룹니다.
- [DDIA Distributed Systems](ddia-distributed-systems/README.md): 01~08까지 RPC, replication, routing, consensus-lite, quorum, election, failure handling을 다룹니다.
- [Shared Utilities](shared/README.md): 여러 Go 프로젝트가 함께 쓰는 hash, file I/O, serializer helper를 정리합니다.

## 읽는 순서

- 먼저 [docs/catalog/project-catalog.md](../docs/catalog/project-catalog.md)에서 전체 문제와 검증 명령을 훑습니다.
- 그다음 원하는 트랙 README로 내려가 프로젝트 표를 읽고, 각 프로젝트 README 첫 화면의 `문제 / 내 해법 / 검증`을 확인합니다.
- 세부 판단이 필요할 때만 `docs/`와 `notion/`으로 내려갑니다.

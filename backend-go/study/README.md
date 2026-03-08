# Study Curriculum

이 트리는 `legacy/`를 그대로 보존하면서, 완전 초보가 Go 백엔드 주니어 후반까지
도달할 수 있도록 재설계한 실제 학습 트리다. `17`번까지는 직접 학습 목표이고,
`18`번은 채용용 대표 포트폴리오를 위한 선택 트랙이다.

## Goal

- 직접 목표: Go 백엔드 주니어 후반
- 비목표: 운영 경험을 포함한 미드급 완성
- 후속 선택 트랙: 채용 공고 제출용 대표 포트폴리오

## Tracks

1. [00-go-fundamentals](00-go-fundamentals/README.md)
2. [01-backend-core](01-backend-core/README.md)
3. [02-distributed-systems](02-distributed-systems/README.md)
4. [03-platform-engineering](03-platform-engineering/README.md)
5. [04-capstone](04-capstone/README.md)
6. [05-portfolio-projects](05-portfolio-projects/README.md)

## Verification Policy

- `verified`는 README에 적힌 핵심 명령을 실제로 실행해 통과한 과제만 사용한다.
- 외부 인프라가 필요한 과제는 현재 로컬 조건에 따라 `partial`로 남길 수 있다.

## Workspace

`go.work`는 이 저장소의 학습 모듈만 묶는다. legacy 워크스페이스는 건드리지 않는다.

## Commands

```bash
make test-new
make test-migrated
make test-all
make test-infra
make test-portfolio-unit
make test-portfolio-repro
```

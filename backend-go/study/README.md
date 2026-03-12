# Study Curriculum

`study/`는 이 저장소의 활성 커리큘럼이다. 루트 README가 대표작과 전체 방향을 보여 준다면, 이 문서는 5개 트랙 18개 프로젝트를 어떤 순서로 읽어야 하는지 안내한다.

## 이 커리큘럼이 푸는 문제

- Go 백엔드 학습이 문법, API, DB, 분산 시스템, 배포로 점프하면서 자주 끊어진다는 문제
- 프로젝트는 많은데 선수 지식과 학습 순서가 불분명하다는 문제
- 완성된 capstone과 포트폴리오가 앞 단계 과제와 어떻게 연결되는지 흐려진다는 문제

## 이 커리큘럼의 답

- `00-go-fundamentals`에서 문법과 테스트 루프를 고정한다.
- `01-backend-core`에서 HTTP, SQL, auth, cache, observability, concurrency를 단계적으로 쌓는다.
- `02-distributed-systems`와 `03-platform-engineering`에서 계약, 로그 구조, 정합성, 이벤트, 배포 자산으로 확장한다.
- `04-capstone`과 `05-portfolio-projects`에서 필수 기준선과 채용용 대표작을 각각 만든다.

## 트랙 순서

1. [00-go-fundamentals](00-go-fundamentals/README.md)
2. [01-backend-core](01-backend-core/README.md)
3. [02-distributed-systems](02-distributed-systems/README.md)
4. [03-platform-engineering](03-platform-engineering/README.md)
5. [04-capstone](04-capstone/README.md)
6. [05-portfolio-projects](05-portfolio-projects/README.md)

## 검증 진입점

```bash
make test-new
make test-migrated
make test-infra
make test-runtime
make test-portfolio-unit
make test-portfolio-repro
```

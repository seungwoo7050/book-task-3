# backend-go study blog

`study/blog/`는 `backend-go`의 독립 프로젝트를 source-first chronology로 다시 쓰는 레이어다. 이 재생성은 README, `problem/`, `solution/`, `docs/`, 테스트, 현재 CLI 출력만을 근거로 삼고 기존 blog 초안은 입력 자료에서 제외했다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 배치 재작성 원칙

- 기존 blog 처리 방식: `isolate-and-rewrite`
- 처리 기준: 프로젝트 README, problem 문서, 구현 진입점, 검증 명령이 모두 있는 가장 작은 랩 디렉터리
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## 트랙 인덱스

- [00 Go Fundamentals](00-go-fundamentals/README.md)
- [01 Backend Core](01-backend-core/README.md)
- [02 Distributed Systems](02-distributed-systems/README.md)
- [03 Platform Engineering](03-platform-engineering/README.md)
- [04 Capstone](04-capstone/README.md)
- [05 Portfolio Projects](05-portfolio-projects/README.md)

## 처리 수

- 처리한 프로젝트: 18
- 건너뛴 디렉터리: 8

## 건너뛴 디렉터리

- `docs`: 공용 문서 디렉터리라 독립 프로젝트가 아니다.
- `study`: 커리큘럼 전체를 설명하는 집합 루트라 프로젝트 단위가 아니다.
- `study/00-go-fundamentals`: 여러 랩을 묶는 트랙 디렉터리라 독립 프로젝트 기준에 맞지 않았다.
- `study/01-backend-core`: 여러 랩을 묶는 트랙 디렉터리라 독립 프로젝트 기준에 맞지 않았다.
- `study/02-distributed-systems`: 여러 랩을 묶는 트랙 디렉터리라 독립 프로젝트 기준에 맞지 않았다.
- `study/03-platform-engineering`: 여러 랩을 묶는 트랙 디렉터리라 독립 프로젝트 기준에 맞지 않았다.
- `study/04-capstone`: 여러 랩을 묶는 트랙 디렉터리라 독립 프로젝트 기준에 맞지 않았다.
- `study/05-portfolio-projects`: 여러 랩을 묶는 트랙 디렉터리라 독립 프로젝트 기준에 맞지 않았다.

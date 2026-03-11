# docs

루트 `docs/`는 `cs-core/study` 전체에 공통으로 적용되는 공개 규칙과 커리큘럼 설명을 둔다.
트랙별 구현 reasoning이나 프로젝트별 디버그 기록은 각 디렉터리의 `docs/`, `notion/`으로 내려 보낸다.

## 먼저 읽을 문서

1. [`curriculum-map.md`](curriculum-map.md)
2. [`repository-architecture.md`](repository-architecture.md)
3. [`readme-contract.md`](readme-contract.md)
4. [`status-matrix.md`](status-matrix.md)

## 문서 역할

- `curriculum-map.md`: 4개 트랙과 15개 프로젝트를 어떤 순서로 읽는지 설명한다.
- `repository-architecture.md`: `problem/`, 구현 디렉터리, `docs/`, `notion/`, `notion-archive/`의 책임을 고정한다.
- `readme-contract.md`: 루트, 트랙, 프로젝트 README가 따라야 할 공개 표면 계약을 명시한다.
- `status-matrix.md`: 프로젝트별 현재 상태와 대표 검증 경로를 한눈에 보여 준다.

로컬 전용 복원 스크립트와 Docker 빌드 자산은 `docs/`가 아니라 `scripts/` 아래에 둔다.

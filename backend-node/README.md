# backend-node

이 저장소는 `legacy/`에 남아 있는 기존 Node.js 백엔드 학습 트리를 보존하면서,
`study/` 아래에 완전 초보부터 Node.js 백엔드 주니어 준비와 미드 초입 개념까지
이어지는 새 학습 커리큘럼을 재구성하는 저장소다.

## 디렉터리 역할

- `legacy/`: 기존 학습 트리. 읽기 전용 참조 자료.
- `study/`: 새 학습 경로와 구현 작업 공간.
- `docs/`: 저장소 공통 규칙, 커리큘럼 지도, 감사 결과.

## 현재 진입점

1. `docs/README.md`
2. `docs/curriculum-map.md`
3. `study/README.md`
4. `study/Node-Backend-Architecture/README.md`

## 현재 상태

- `legacy/`는 보존했다.
- `study/Node-Backend-Architecture/` 트랙을 00~10 프로젝트까지 실제 실행 가능한 형태로 정리했다.
- `03`~`09`의 legacy 기반 프로젝트는 문제 자료와 구현 코드를 `node_modules` 없이 옮겼다.
- `00`, `01`, `02`, `08`은 신규 설계 프로젝트로 starter code, 구현, 테스트를 추가했다.
- `00`~`10`은 현재 새 경로에서 다시 빌드와 테스트를 통과한 `verified` 상태다.
- `06`, `07`, `09`는 `better-sqlite3` native build 승인 절차가 필요하므로 설치 순서를 README에 명시했다.
- `10-shippable-backend-service`는 `09-platform-capstone`을 채용 제출용 서비스 형태로 강화한 Postgres + Redis + Docker Compose 기반 프로젝트다.
- `06`, `07`, `09`의 sqlite 복구 절차는 [native-sqlite-recovery.md](/Users/woopinbell/work/backend-node/study/Node-Backend-Architecture/docs/native-sqlite-recovery.md)에 공통 가이드로 정리했다.
- 각 프로젝트의 `notion/`은 템플릿이 아니라 공개 가능한 기술 노트 초안으로 채웠다.

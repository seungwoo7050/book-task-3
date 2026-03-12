# 03-rest-api-foundations

- 그룹: `Core`
- 상태: `verified`
- 공개 답안 레인: `express/`, `nestjs/`
- 성격: 초기 원본 이관 + 재검증

## 한 줄 문제

같은 Books CRUD 문제를 Express와 NestJS로 각각 풀며 계층 분리, DI, 테스트 기본을 비교하는 첫 비교 학습 문제다.

## 성공 기준

- Router/Controller/Service 경계를 설명하고 구현할 수 있다.
- Express의 수동 DI와 NestJS의 container DI 차이를 코드로 비교할 수 있다.
- 단위 테스트와 e2e 테스트로 CRUD 계약을 재현할 수 있다.

## 내가 만든 답

- `express/`에서는 composition root를 드러내는 수동 DI 구조로 CRUD를 구현했다.
- `nestjs/`에서는 module, controller, service를 분리해 같은 문제를 framework DI로 구현했다.
- `problem/`에는 starter code를, `docs/`에는 비교 개념 문서를, `notion/`에는 긴 서사를 남겨 읽기 층을 분리했다.

## 제공 자료

- `problem/README.md`와 starter code
- `express/`
- `nestjs/`
- `docs/`
- `notion/`

## 실행과 검증

### Express 레인
- 작업 디렉터리: `express/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test`
- run: `pnpm run dev` 또는 `pnpm run start`

### NestJS 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run start:dev` 또는 `pnpm run start`

## 왜 다음 단계로 이어지는가

- `04-request-pipeline`에서 CRUD 자체보다 요청 검증과 오류 규약을 먼저 고정한다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [express/README.md](express/README.md), [nestjs/README.md](nestjs/README.md)에서 확인한다.

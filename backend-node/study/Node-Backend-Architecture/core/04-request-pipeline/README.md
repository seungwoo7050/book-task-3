# 04-request-pipeline

- 그룹: `Core`
- 상태: `verified`
- 공개 답안 레인: `express/`, `nestjs/`
- 성격: 초기 원본 이관 + 재검증

## 한 줄 문제

validation, error handling, logging, response shaping을 요청 파이프라인 규약으로 묶어 이후 모든 API의 공통 기반을 만드는 문제다.

## 성공 기준

- 요청이 들어와서 성공 또는 실패 응답으로 나갈 때의 공통 규약을 설명할 수 있다.
- Express middleware 순서와 NestJS pipe/filter/interceptor 순서를 비교할 수 있다.
- e2e 테스트로 응답 envelope와 오류 형식을 고정할 수 있다.

## 내가 만든 답

- 두 레인 모두 validation, error response, logging, response wrapper를 공통 규약으로 구현했다.
- auth보다 앞 단계에 두어 실패 경로와 응답 형식을 먼저 고정하게 했다.
- `docs/`에는 Express/NestJS 파이프라인 개념 문서를, `notion/`에는 재현 로그를 남겼다.

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
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run dev`

### NestJS 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run start:dev`

## 왜 다음 단계로 이어지는가

- `05-auth-and-authorization`에서 같은 요청 파이프라인 위에 JWT와 RBAC 규칙을 올린다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [express/README.md](express/README.md), [nestjs/README.md](nestjs/README.md)에서 확인한다.

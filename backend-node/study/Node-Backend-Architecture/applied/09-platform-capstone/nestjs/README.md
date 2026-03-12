# NestJS capstone 구현

## 담당 범위

여러 코어 단계의 규약을 단일 서비스로 다시 조합하는 통합 적용 레인이다.

## 현재 구조

- `src/`: auth, books, events, persistence module
- `test/`: unit/e2e capstone 검증

## 실행과 검증

- install: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3`
- build: `pnpm run build`
- test: `pnpm run test`
- e2e: `pnpm run test:e2e`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.

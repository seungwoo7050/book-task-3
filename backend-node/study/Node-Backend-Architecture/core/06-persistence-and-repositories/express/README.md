# Express 구현

## 담당 범위

raw SQL과 직접 만든 repository를 통해 저장 계층 경계를 눈으로 볼 수 있게 하는 레인이다.

## 현재 구조

- `src/`: repository, service, route 계층
- `test/`: unit/e2e + DB 검증

## 실행과 검증

- install: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3`
- build: `pnpm run build`
- test: `pnpm run test`
- e2e: `pnpm run test:e2e`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.

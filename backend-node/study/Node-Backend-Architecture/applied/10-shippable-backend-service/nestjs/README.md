# NestJS 포트폴리오 구현

## 담당 범위

채용 제출용으로 바로 읽히는 서비스 표면을 목표로 하는 단일 적용 레인이다.

## 현재 구조

- `src/`: auth, books, events, runtime 모듈
- `test/`: unit/e2e 검증
- `ci/`: service container 기반 검증

## 실행과 검증

- install: `pnpm install`
- build: `pnpm run build`
- migrate: `pnpm run db:migrate`
- seed: `pnpm run db:seed`
- test: `pnpm run test`
- e2e: `pnpm run test:e2e`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.

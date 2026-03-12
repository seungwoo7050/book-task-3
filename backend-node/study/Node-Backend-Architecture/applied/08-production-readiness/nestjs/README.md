# NestJS 운영성 구현

## 담당 범위

실무형 NestJS 서비스에 운영 준비 요소를 덧붙이는 단일 적용 레인이다.

## 현재 구조

- `src/`: config, health, logging, app wiring
- `tests/`: unit/e2e 운영성 검증
- `ci/`: GitHub Actions 예시

## 실행과 검증

- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- e2e: `pnpm run test:e2e`
- run: `pnpm run start`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.

# 03-rest-api-foundations

- 상태: `verified`
- 구현 레인: `express/`, `nestjs/`
- legacy 출처: `legacy/01-rest-api`

## 목표

Express와 NestJS로 동일한 CRUD API를 구현하면서
계층 분리, DI, 테스트 기본을 비교 학습한다.

## 현재 상태

- 원본 starter code와 Makefile
- Express solution 코드와 테스트
- NestJS solution 코드와 테스트
- legacy docs를 옮긴 개념 문서

## 실행 명령

- `express/`: `pnpm install && pnpm run build && pnpm run test`
- `nestjs/`: `pnpm install && pnpm run build && pnpm run test && pnpm run test:e2e`

## 검증 상태

- `express/`: `pnpm run build && pnpm run test`
- `nestjs/`: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 실패 시 복구 루트

- Express strict 타입 오류가 나면 controller에서 `req.params`와 service 반환 타입을 먼저 본다.
- NestJS 테스트가 실패하면 DTO/entity strict 설정과 controller/service wiring부터 확인한다.

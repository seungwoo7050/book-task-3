# 04-request-pipeline

- 상태: `verified`
- 구현 레인: `express/`, `nestjs/`
- legacy 출처: `legacy/03-pipeline`

## 목표

validation, error handling, logging, response shaping을
요청 파이프라인으로 묶어 공통 규약의 중요성을 학습한다.

## 왜 auth보다 먼저 두는가

초보는 인증 흐름보다 먼저 요청이 어떻게 검증되고 실패하는지 이해해야 한다.
이 프로젝트는 이후 auth, DB, capstone에서 재사용되는 규약의 기반이다.

## 현재 상태

- Express/NestJS starter code
- solution 코드와 테스트
- 개념 문서와 비교 문서

## 실행 명령

- `express/`: `pnpm install && pnpm run build && pnpm run test && pnpm run test:e2e`
- `nestjs/`: `pnpm install && pnpm run build && pnpm run test && pnpm run test:e2e`

## 검증 상태

새 경로에서 아래 검증을 다시 통과시켰다.

- `express/`: `pnpm run build && pnpm run test && pnpm run test:e2e`
- `nestjs/`: `pnpm run build && pnpm run test && pnpm run test:e2e`

## 실패 시 복구 루트

- 검증 오류가 나면 middleware/pipe 순서와 예외 변환 지점을 먼저 확인한다.
- E2E가 깨지면 응답 래퍼와 글로벌 예외 처리기 응답 형태가 테스트 기대치와 같은지 본다.

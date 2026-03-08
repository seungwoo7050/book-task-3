# 00-language-and-typescript

- 상태: `verified`
- 구현 레인: `ts/`
- 신규 설계 여부: 신규 프로젝트

## 목표

JavaScript와 TypeScript의 핵심 문법, 비동기 흐름, 타입 모델링을 먼저 익혀
후속 Express/NestJS 프로젝트에서 언어 자체가 병목이 되지 않게 만든다.

## 범위

- 함수, 객체, 배열 변환
- `Promise`, `async/await`, 에러 처리
- `type`, `interface`, module, import/export
- 간단한 CLI와 테스트

## 현재 상태

문제 설명, starter code, TypeScript 구현, 테스트를 추가했고 새 경로에서 다시 검증했다.

## 실행 명령

- 구현 경로: `ts/`
- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- cli: `pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"`

## 검증 상태

- `ts/`: `pnpm run build && pnpm run test`

## 실패 시 복구 루트

- TypeScript strict 오류가 나면 선택적 필드와 비동기 반환 타입부터 확인한다.
- CLI 인자 파싱이 실패하면 `--title`, `--author`, `--year`, `--tags` 형식이 맞는지 먼저 본다.

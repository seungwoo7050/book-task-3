# TypeScript Implementation

## 범위

초보용 TypeScript 실습 함수와 작은 CLI를 제공한다.

## 현재 상태

- 상태: `verified`
- build: `pnpm run build`
- test: `pnpm run test`
- cli: `pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"`

## 포함된 것

- `src/catalog.ts`: 타입 모델링과 비동기 inventory 처리
- `src/cli.ts`: 인자 파싱과 출력 포맷팅
- `tests/catalog.test.ts`: 동기/비동기/CLI 동작 검증

## 알려진 제약

- CLI는 학습용이므로 간단한 `--flag value` 규약만 지원한다.

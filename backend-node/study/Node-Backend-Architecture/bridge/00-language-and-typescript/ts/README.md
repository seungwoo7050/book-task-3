# TypeScript 구현

## 담당 범위

도메인 타입, CLI 입력 파싱, 테스트를 한 워크스페이스 안에 묶어 언어 자체를 익히는 레인이다.

## 현재 구조

- `src/`: 타입, 유틸리티, CLI 진입점
- `tests/`: 언어 기능과 CLI 동작 검증

## 실행과 검증

- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- cli: `pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.

# Node 구현

## 담당 범위

런타임 입출력과 스크립트 실행 환경을 직접 다루는 단일 구현 레인이다.

## 현재 구조

- `src/`: 로그 파서, 요약기, CLI 진입점
- `tests/`: 파일 입력과 출력 형식 검증

## 실행과 검증

- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- cli: `REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.

# Node Implementation

## 범위

파일 입력과 env 기반 동작을 다루는 NDJSON 요약 CLI를 제공한다.

## 현재 상태

- 상태: `verified`
- build: `pnpm run build`
- test: `pnpm run test`
- cli: `REPORT_FORMAT=text pnpm start -- ../problem/data/request-log.ndjson`

## 포함된 것

- `src/request-report.ts`: 스트리밍 파서와 요약 계산
- `src/cli.ts`: env/argv 처리
- `tests/request-report.test.ts`: 파일 처리와 출력 형식 검증

## 알려진 제약

- 학습용 구현이라 gzip, CSV, 복수 파일 입력은 지원하지 않는다.

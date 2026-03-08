# 01-node-runtime-and-tooling

- 상태: `verified`
- 구현 레인: `node/`
- 신규 설계 여부: 신규 프로젝트

## 목표

Node.js 런타임과 도구 체인을 이해해 작은 스크립트와 CLI를 직접 다룰 수 있게 만든다.

## 범위

- `process.env`
- `fs`, `path`, streams 기초
- package manager, scripts, debugging
- 기본 테스트 러너 사용

## 현재 상태

NDJSON 요청 로그를 읽어 요약하는 CLI와 테스트를 추가했고 새 경로에서 다시 검증했다.

## 실행 명령

- 구현 경로: `node/`
- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- cli: `REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson`

## 검증 상태

- `node/`: `pnpm run build && pnpm run test`

## 실패 시 복구 루트

- 파일을 찾지 못하면 CLI 인자로 넘긴 경로가 구현 디렉터리 기준이 아니라 현재 셸 기준임을 먼저 확인한다.
- JSON 파싱 오류가 나면 `problem/data/request-log.ndjson` 형식이 한 줄당 하나의 JSON 객체인지 확인한다.

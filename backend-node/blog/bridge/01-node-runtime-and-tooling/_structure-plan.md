# 01-node-runtime-and-tooling structure plan

이 문서는 Node 런타임 API 나열이 아니라, 파일 입력과 env를 다루는 작은 운영 도구가 어떻게 서는지 보여 줘야 한다. 중심은 `stream -> summary -> CLI` 흐름이다.

## 읽기 구조

1. line-oriented parsing이 왜 먼저 나오는지 잡는다.
2. route/user/error를 어떤 운영 지표로 선택했는지 보여 준다.
3. `REPORT_FORMAT`와 파일 경로가 CLI 계약으로 닫히는 장면으로 마무리한다.

## 반드시 남길 근거

- `readRequestLog`
- `summarizeRequests`
- `formatSummary`
- `runCli`
- `pnpm run build`
- `pnpm run test`
- `node dist/cli.js ../problem/data/request-log.ndjson`

## 리라이트 톤

- "Node API를 배웠다"보다 "어떤 입력을 어떤 계약으로 다뤘는가"가 먼저 보이게 쓴다.
- 로그 요약은 기능 설명보다 지표 선택의 이유가 드러나게 정리한다.

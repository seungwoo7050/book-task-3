# 01-node-runtime-and-tooling evidence ledger

이 프로젝트도 `git log`에는 `2026-03-12`의 이관 커밋만 남아 있다. chronology는 `request-report.ts`, `cli.ts`, 테스트, 그리고 실제 재검증 명령을 따라 다시 세운 것이다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | NDJSON 로그를 줄 단위로 안전하게 읽는다 | `node/src/request-report.ts`의 `readRequestLog` | 작은 예제니까 파일 전체를 한 번에 읽어도 충분해 보였다 | `createReadStream`과 `readline`으로 line-oriented parser를 만들고 line number를 오류 메시지에 남겼다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build` | `build: ok` | `for await (const line of lineReader)` | 파일 입력은 성공보다 "어디서 깨졌는가"를 알려 주는 편이 더 중요하다 | 읽은 로그를 운영 지표처럼 요약해야 한다 |
| 2 | Phase 2 | 요청 로그를 사람이 읽는 요약으로 바꾼다 | `node/src/request-report.ts`의 `summarizeRequests`, `formatSummary` | route count만 세면 학습용 도구로는 충분할 것 같았다 | unique users, error count, perRoute를 함께 계산하고 text/json 두 출력 모드를 만들었다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` | `Test Files 1 passed`, `Tests 5 passed` | `perRoute[record.route] = (perRoute[record.route] ?? 0) + 1` | 로그 요약은 count를 세는 일이 아니라 "무엇을 지표로 볼지"를 정하는 일이다 | env와 argv를 받는 CLI 입구가 필요하다 |
| 3 | Phase 3 | 파일 경로와 출력 포맷을 CLI 계약으로 묶는다 | `node/src/cli.ts`, `node/tests/request-report.test.ts` | 파일 경로 하나만 받으면 도구 표면은 충분해 보였다 | `REPORT_FORMAT`, 잘못된 포맷, 누락된 경로를 모두 명시적 오류로 바꾸고 compiled CLI로 재검증했다 | `COREPACK_ENABLE_AUTO_PIN=0 node dist/cli.js ../problem/data/request-log.ndjson` | `Total requests: 5`, `Unique users: 3`, `Error count: 2` | `const requestedFormat = env.REPORT_FORMAT ?? "text"` | Node 런타임의 실제 입구는 함수 시그니처보다 env와 argv 검증에 더 가까웠다 | 다음 프로젝트에서 이 감각을 HTTP request/response로 옮긴다 |

## 근거 파일

- `bridge/01-node-runtime-and-tooling/README.md`
- `bridge/01-node-runtime-and-tooling/problem/README.md`
- `bridge/01-node-runtime-and-tooling/node/src/request-report.ts`
- `bridge/01-node-runtime-and-tooling/node/src/cli.ts`
- `bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts`

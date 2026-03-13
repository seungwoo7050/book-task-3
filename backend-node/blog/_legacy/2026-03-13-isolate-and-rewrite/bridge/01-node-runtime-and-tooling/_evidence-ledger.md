# 01-node-runtime-and-tooling evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/README.md), [`node/src/request-report.ts`](../../../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/request-report.ts), [`node/src/cli.ts`](../../../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/cli.ts), [`node/tests/request-report.test.ts`](../../../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts), `problem/data/request-log.ndjson`, 실제 CLI 출력뿐이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: Node 런타임에서 파일을 한 줄씩 읽는 가장 작은 패턴을 익힌다.
- 변경 단위: `node/src/request-report.ts`
- 처음 가설: 작은 로그 파일이어도 `readFile()`보다 stream + `readline`으로 가야 다음 로그/queue 작업과 자연스럽게 이어진다.
- 실제 조치: `readRequestLog()`가 `stat()`, `createReadStream()`, `readline.createInterface()`를 사용해 NDJSON을 한 줄씩 파싱하고 line number까지 포함한 오류를 만든다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`
- 검증 신호: `tsc` 통과.
- 핵심 코드 앵커: `readRequestLog()`
- 새로 배운 것: 이 프로젝트의 핵심은 JSON 자체보다 "Node에서 file path, stream, line iterator를 안전하게 다루는 표면"이었다.
- 다음: 읽어 온 record를 summary와 출력 포맷으로 묶는다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: 단순 파싱을 넘어 per-route, unique user, error count를 요약한다.
- 변경 단위: `node/src/request-report.ts`
- 처음 가설: summary 구조를 먼저 고정해 두면 text와 JSON 출력 포맷을 같은 데이터에서 뽑을 수 있다.
- 실제 조치: `summarizeRequests()`가 `Set`과 `perRoute` 맵을 만들고, `formatSummary()`가 `text | json` 두 formatter를 지원한다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: `✓ tests/request-report.test.ts (5 tests)`, `Tests 5 passed (5)`
- 핵심 코드 앵커: `summarizeRequests()`, `formatSummary()`
- 새로 배운 것: 런타임 프로젝트에서도 먼저 고정할 것은 화면 출력이 아니라 "어떤 summary shape를 외부 계약으로 둘 것인가"였다.
- 다음: env와 CLI 인자를 붙여 실행 entrypoint를 닫는다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: path 입력과 env 기반 출력 포맷을 하나의 CLI로 묶는다.
- 변경 단위: `node/src/cli.ts`, `node/tests/request-report.test.ts`
- 처음 가설: `REPORT_FORMAT` 하나만 열어 두면 text/json 두 출력 모드를 런타임 감각과 함께 보여 줄 수 있다.
- 실제 조치: `runCli()`가 path 유무와 `REPORT_FORMAT` 값을 검증하고, 성공 시 summary를 출력한다.
- CLI: `REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson`
- 검증 신호: `totalRequests: 5`, `uniqueUsers: 3`, `errorCount: 2`
- 핵심 코드 앵커: `runCli()`
- 새로 배운 것: CLI adapter는 인자를 받는 코드보다 "입력 경로, env, 오류 메시지"를 어떤 순서로 검증할지까지 포함한다.
- 다음: [`../02-http-and-api-basics/00-series-map.md`](../02-http-and-api-basics/00-series-map.md)에서 파일 입력 대신 HTTP request/response를 직접 받기 시작한다.

# 01-node-runtime-and-tooling Evidence Ledger

## 독립 Todo 판정
- 판정: `done`
- 이유: `problem/README.md`가 별도 성공 기준을 가진 독립 bridge 문제이고, `node/` 워크스페이스가 자체 build/test/CLI surface를 갖는다.
- 이번 Todo에서도 기존 blog 본문은 입력 근거로 사용하지 않았다.

## 이번 턴에 읽은 근거
- `backend-node/README.md`
- `backend-node/study/Node-Backend-Architecture/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/data/request-log.ndjson`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/script/run-example.sh`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/package.json`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/request-report.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/cli.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/docs/concepts/streaming-cli.md`

## 소스에서 확인한 핵심 사실
- 이 프로젝트의 핵심은 Node API 나열이 아니라 파일과 env를 신뢰하지 않는 CLI 계약이다.
- `readRequestLog()`는 `path.resolve()`와 `stat()`로 파일 존재를 먼저 확인한 뒤, `createReadStream + readline`으로 줄 단위 parsing을 수행한다.
- JSON 파싱 실패는 `Invalid JSON at line N` 형태로 line number를 포함한 오류가 된다.
- summary는 `totalRequests`, `uniqueUsers`, `errorCount`, `perRoute` 네 숫자를 남긴다.
- `formatSummary()`는 같은 summary를 text/json 두 출력 표면으로 나눈다.
- `runCli()`는 `REPORT_FORMAT` 허용값을 `text | json`으로 제한하고, 잘못된 값이면 stderr와 exit code `1`을 돌린다.
- 구현은 `args[0]`을 파일 경로로 기대한다.
- README와 `problem/script/run-example.sh`는 `pnpm start -- <path>`를 사용 예로 제시하지만, 현재 구현에서는 `--`가 파일 경로로 들어가 `ENOENT`를 일으킨다.
- `run-example.sh`는 상위 문제 폴더에서 실행하면 `package.json`이 없는 cwd 문제까지 추가로 겪는다.

## 검증 명령과 실제 결과

| 명령 | 결과 | 메모 |
| --- | --- | --- |
| `pnpm run build` | 통과 | `tsc` exit code `0` |
| `pnpm run test` | 통과 | `1` file, `5` tests passed |
| `REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson` | 통과 | JSON summary 출력 확인 |
| `node dist/cli.js ../problem/data/request-log.ndjson` | 통과 | text summary 출력 확인 |
| `REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson` | 실패 | `--`를 파일 경로로 읽어 `ENOENT ... /node/--` |
| `bash problem/script/run-example.sh` | 실패 | 상위 폴더에서는 `No package.json`, `node/` 내부에서는 같은 `--` 인자 문제 재현 |

## 이번 문서가 기대는 중심 앵커
- parser 앵커: `node/src/request-report.ts`
- CLI 계약 앵커: `node/src/cli.ts`
- fixture 앵커: `problem/data/request-log.ndjson`
- 테스트 앵커: `node/tests/request-report.test.ts`

## 이번 턴의 품질 메모
- build/test 성공만 적지 않고, README와 스크립트의 실제 재현 경로가 깨지는 점까지 함께 기록했다.
- line-oriented parser의 의미를 메모리 최적화보다 "어디서 깨졌는지 설명하는 능력"으로 다시 정리했다.
- direct `node dist/cli.js` 성공과 `pnpm start -- ...` 실패를 구분해 구현과 문서 표면을 분리했다.

# 01-node-runtime-and-tooling 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 NDJSON 로그를 줄 단위로 읽고 집계 결과를 출력할 것, 출력 포맷과 파일 경로 오류를 테스트로 검증할 것, README의 단일 명령으로 실행 흐름을 다시 재현할 수 있을 것을 한 흐름으로 설명하고 검증한다. 핵심은 `runCli`와 `readRequestLog`, `summarizeRequests` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- NDJSON 로그를 줄 단위로 읽고 집계 결과를 출력할 것
- 출력 포맷과 파일 경로 오류를 테스트로 검증할 것
- README의 단일 명령으로 실행 흐름을 다시 재현할 수 있을 것
- 첫 진입점은 `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/cli.ts`이고, 여기서 `runCli`와 `readRequestLog` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/cli.ts`: `runCli`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/request-report.ts`: `readRequestLog`, `summarizeRequests`, `formatSummary`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/code/starter.ts`: `readRequestLog`, `summarizeRequests`, `formatSummary`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts`: `fixturePath`, `request report`, `reads NDJSON records from disk`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/pnpm-lock.yaml`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tsconfig.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/data/request-log.ndjson`: 핵심 구현을 담는 파일이다.
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/package.json`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/code/starter.ts`와 `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/cli.ts`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `fixturePath` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node && npm run test -- --run
```

- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/code/starter.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `fixturePath`와 `request report`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/cli.ts`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/request-report.ts`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/code/starter.ts`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/pnpm-lock.yaml`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tsconfig.json`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/data/request-log.ndjson`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/script/run-example.sh`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/package.json`
- `../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/vitest.config.ts`

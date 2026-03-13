# 01-node-runtime-and-tooling series map

이 프로젝트는 TypeScript 안에서 정리하던 값을 실제 파일과 env, stream이 섞인 런타임으로 끌고 나오는 단계다. 질문은 간단하다. "디스크의 NDJSON 로그를 읽고, 요약하고, CLI로 내보내는 작은 도구를 어디까지 단단하게 만들 수 있을까?"

처음에는 `request-report.ts`를 읽는 편이 좋다. 이 파일에서 입력을 한 줄씩 읽고, route와 user 기준으로 요약하는 흐름이 잡히면 `cli.ts`가 어떤 표면을 닫는지 바로 이어진다.

## 이 글에서 볼 것

- `readline`과 stream으로 NDJSON를 line-oriented하게 읽는 이유
- `totalRequests`, `uniqueUsers`, `errorCount`, `perRoute`를 왜 함께 남겼는지
- `REPORT_FORMAT`와 파일 경로를 CLI가 어떻게 검증하는지

## source of truth

- `bridge/01-node-runtime-and-tooling/README.md`
- `bridge/01-node-runtime-and-tooling/problem/README.md`
- `bridge/01-node-runtime-and-tooling/node/src/request-report.ts`
- `bridge/01-node-runtime-and-tooling/node/src/cli.ts`
- `bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts`

## 구현 흐름 한눈에 보기

1. NDJSON를 stream + `readline`으로 한 줄씩 읽는다.
2. 읽은 레코드를 route/user/error 지표로 요약한다.
3. CLI에서 파일 경로와 출력 포맷을 검증하고 결과를 출력한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
build: ok

$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       5 passed (5)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 node dist/cli.js ../problem/data/request-log.ndjson
File: /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/problem/data/request-log.ndjson
Total requests: 5
Unique users: 3
Error count: 2
Per route:
- /books: 3
- /books/1: 1
- /health: 1
```

## 다음 프로젝트와의 연결

다음 장 `02-http-and-api-basics`에서는 파일과 env 대신 HTTP request/response를 직접 다룬다. 즉 런타임 입력을 다루는 감각이 이제 네트워크 표면으로 넘어간다.

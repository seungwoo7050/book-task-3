# 01-node-runtime-and-tooling development timeline

이 프로젝트에 들어오면 이전 단계와 분위기가 확 달라진다. 더 이상 메모리 안의 문자열만 다루지 않고, 실제 파일 경로를 받고, 스트림을 열고, env에 따라 출력 형식을 바꾸기 시작한다. 소스를 따라가 보면 구현 순서는 놀라울 정도로 단순하다. 먼저 NDJSON을 한 줄씩 읽는 reader를 만들고, 그다음 summary model을 세운 뒤, 마지막에 CLI와 env를 붙였다.

## 구현 순서 요약

- NDJSON 파일을 `createReadStream()`과 `readline`으로 읽는다.
- record 배열을 route/user/error 기준 summary로 축약한다.
- `REPORT_FORMAT`과 파일 경로를 받는 CLI adapter로 런타임 표면을 닫는다.

## Phase 1

- 당시 목표: 로그 파일을 통째로 메모리에 올리지 않고 line-by-line으로 읽는다.
- 변경 단위: `node/src/request-report.ts`
- 처음 가설: 작은 연습 프로젝트라도 스트림을 쓰는 편이 다음 로그 처리나 CLI 도구로 넘어갈 때 덜 버린다.
- 실제 진행: `readRequestLog()`가 `path.resolve()`, `stat()`, `createReadStream()`, `readline.createInterface()`를 묶고 빈 줄은 건너뛰며, JSON 파싱 실패 시 line number를 포함해 예외를 던진다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/request-report.test.ts (5 tests)
Tests 5 passed (5)
```

검증 신호:

- fixture `request-log.ndjson`에서 정확히 5개의 record를 읽는다.
- 첫 record의 `route`가 `/books`인지까지 테스트로 고정된다.

핵심 코드:

```ts
const stream = createReadStream(resolvedPath, { encoding: "utf8" });
const lineReader = readline.createInterface({
  input: stream,
  crlfDelay: Number.POSITIVE_INFINITY,
});

for await (const line of lineReader) {
  lineNumber += 1;
  if (line.trim().length === 0) {
    continue;
  }
```

왜 이 코드가 중요했는가:

여기서부터 프로젝트는 "파일을 받는 런타임 도구"가 된다. 이후에 summary나 formatter를 아무리 잘 짜도, 이 reader가 path와 line boundary를 제대로 다루지 못하면 전체 도구가 흔들린다.

새로 배운 것:

- Node 런타임의 기본기는 HTTP 서버보다 먼저 `fs`, stream, iterator를 안전하게 엮는 감각에서 나온다.

## Phase 2

- 당시 목표: 읽은 record를 사람이 설명할 수 있는 summary shape로 압축한다.
- 변경 단위: `node/src/request-report.ts`
- 처음 가설: formatter를 먼저 쓰면 text/json 출력이 서로 다른 규칙으로 갈라지기 쉽다. summary object를 먼저 만들면 두 출력 모드가 같은 근거를 공유한다.
- 실제 진행: `summarizeRequests()`가 `Set`으로 unique user를 세고 `perRoute`를 누적하며, `formatSummary()`가 text와 JSON 두 포맷을 처리한다.

CLI:

```bash
$ REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson
{
  "totalRequests": 5,
  "uniqueUsers": 3,
  "errorCount": 2,
  "perRoute": {
    "/books": 3,
    "/books/1": 1,
    "/health": 1
  }
}
```

검증 신호:

- `/books`가 3회, `/books/1`이 1회, `/health`가 1회라는 route 분포가 그대로 출력된다.
- 에러는 status code `>= 400` 기준으로 2회 집계된다.

핵심 코드:

```ts
for (const record of records) {
  uniqueUsers.add(record.userId);
  perRoute[record.route] = (perRoute[record.route] ?? 0) + 1;

  if (record.status >= 400) {
    errorCount += 1;
  }
}
```

왜 이 코드가 중요했는가:

summary shape를 먼저 고정했기 때문에 text formatter도 JSON formatter도 같은 데이터를 재사용한다. 이게 이후 API 응답 envelope를 설계할 때 그대로 반복되는 패턴이다.

새로 배운 것:

- 출력 형식은 마지막 단계고, 진짜 계약은 "어떤 aggregate를 외부에 보일 것인가"다.

## Phase 3

- 당시 목표: path 인자와 env 기반 출력 포맷을 실제 CLI로 묶는다.
- 변경 단위: `node/src/cli.ts`, `node/tests/request-report.test.ts`
- 처음 가설: 런타임 도구라면 잘못된 path, 잘못된 env 값, 정상 출력까지 모두 entrypoint에서 닫혀야 한다.
- 실제 진행: `runCli()`가 인자 누락을 검사하고, `REPORT_FORMAT`이 `text | json`이 아니면 바로 stderr를 쓰고 종료한다.

CLI:

```bash
$ REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson
$ pnpm start -- ../problem/data/request-log.ndjson
ENOENT: no such file or directory, stat '.../node/--'
```

검증 신호:

- 직접 `node dist/cli.js`를 호출하면 JSON report가 정상 출력된다.
- 반면 `pnpm start -- <path>`는 `--`가 인자로 남아 path 검증에서 실패했다. 이 프로젝트의 runtime edge가 코드가 아니라 실행 래퍼에서도 생긴다는 걸 보여 주는 장면이다.

핵심 코드:

```ts
const requestedFormat = env.REPORT_FORMAT ?? "text";
if (requestedFormat !== "text" && requestedFormat !== "json") {
  stderr.write("REPORT_FORMAT must be either text or json\n");
  return 1;
}
```

왜 이 코드가 중요했는가:

파일 경로와 env는 둘 다 런타임 입력인데 성격이 다르다. path는 positional arg로, formatter는 env로 받는다고 결정해 두니 CLI 표면이 훨씬 명확해진다.

새로 배운 것:

- CLI 검증은 코드만 보는 것으로 끝나지 않는다. 패키지 매니저가 인자를 어떻게 전달하는지도 runtime surface의 일부다.

다음:

- [`../02-http-and-api-basics/00-series-map.md`](../02-http-and-api-basics/00-series-map.md)에서 파일 대신 HTTP request/response가 새 입력 표면이 된다.

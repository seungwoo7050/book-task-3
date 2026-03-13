# 01-node-runtime-and-tooling development timeline

`00-language-and-typescript`가 메모리 안의 값을 정리하는 연습이었다면, 여기서는 그 감각이 실제 파일과 CLI로 넘어온다. 이 프로젝트를 따라가다 보면 Node 런타임 API를 많이 외웠다는 느낌보다, "입력을 어디까지 믿을 수 없는 것으로 봐야 하는가"를 먼저 배우게 된다.

## 흐름 먼저 보기

1. NDJSON 로그를 한 줄씩 읽는다.
2. 읽은 레코드를 운영 지표처럼 요약한다.
3. CLI가 파일 경로와 출력 포맷을 검증하는 마지막 입구가 된다.

## 파일을 한 줄씩 읽기로 한 장면

가장 먼저 눈에 들어오는 건 `readRequestLog`가 `readFile`이 아니라 stream으로 시작한다는 점이다.

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
  // ...
}
```

여기서 중요한 건 메모리 절약 그 자체보다, 입력을 줄 단위로 따라가면서 어디서 깨졌는지를 정확히 짚을 수 있다는 점이다. 그래서 아래 오류 경로도 자연스럽다.

```ts
throw new Error(`Invalid JSON at line ${lineNumber}: ${message}`);
```

이 문장이 있으면 깨진 로그를 다시 들여다볼 때 "파일이 이상하다"가 아니라 "몇 번째 줄이 문제다"라는 구체적 질문으로 바로 내려갈 수 있다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
build: ok
```

컴파일이 먼저 통과했다는 사실은, 적어도 이 parser가 Node 스트림과 TypeScript 타입 위에서 모순 없이 서 있다는 최소 신호가 된다.

## 운영 지표를 정한 장면

파일을 읽는 것만으로는 도구가 완성되지 않는다. 이 프로젝트가 재미있어지는 지점은 `summarizeRequests`에서 "무엇을 중요한 숫자로 볼 것인가"를 선택할 때다.

```ts
for (const record of records) {
  uniqueUsers.add(record.userId);
  perRoute[record.route] = (perRoute[record.route] ?? 0) + 1;

  if (record.status >= 400) {
    errorCount += 1;
  }
}
```

`perRoute`와 `uniqueUsers`, `errorCount`를 함께 남긴다는 건 이 도구가 단순한 파일 변환기가 아니라 작은 운영 보고 도구가 되기 시작했다는 뜻이다. 어떤 route에 요청이 몰렸는지, 사용자 수가 몇 명인지, 실패가 몇 건인지가 한 화면에 들어오기 때문이다.

출력 모양도 이 지점에서 갈린다.

```ts
export function formatSummary(summary: RequestSummary, format: "text" | "json"): string {
  if (format === "json") {
    return JSON.stringify(summary, null, 2);
  }
  // ...
}
```

JSON은 다른 도구로 넘기기 좋고, text는 사람이 바로 읽기 좋다. 결국 같은 데이터를 어떤 독자에게 건네려는지가 포맷 선택으로 드러난다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       5 passed (5)
Duration    293ms
```

테스트는 fixture 기준으로 `totalRequests = 5`, `uniqueUsers = 3`, `errorCount = 2`라는 숫자를 고정해 둔다. 여기서부터 이 프로젝트는 "대충 맞는 요약"이 아니라 "계약이 있는 요약"이 된다.

## CLI 표면을 닫아 둔 장면

마지막 장면은 `runCli`다. 이 함수가 등장하면서 파일 처리 유틸리티가 실제 명령줄 도구의 형태를 갖는다.

```ts
const requestedFormat = env.REPORT_FORMAT ?? "text";
if (requestedFormat !== "text" && requestedFormat !== "json") {
  stderr.write("REPORT_FORMAT must be either text or json\n");
  return 1;
}
```

이 검사는 작아 보이지만, 런타임 입력을 어디까지 허용할지를 명시한다는 점에서 중요하다. `REPORT_FORMAT=yaml` 같은 애매한 상태를 허용하지 않기로 한 순간, 도구 표면이 선명해진다.

파일 경로도 같은 방식으로 다뤄진다.

```ts
if (!filePath) {
  stderr.write("사용 예: pnpm start -- <path-to-ndjson>\n");
  return 1;
}
```

재검증은 compiled entrypoint를 직접 호출해 확인했다.

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

이 출력은 이 프로젝트가 단순한 Node API 실습을 넘어, 파일과 env를 믿지 않는 작은 운영 도구로 정리됐다는 사실을 보여 준다. 다음 프로젝트에서는 이 감각이 파일 시스템을 벗어나 HTTP request/response로 넘어간다.

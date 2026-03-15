# 01-node-runtime-and-tooling 개발 타임라인

`01-node-runtime-and-tooling`은 TypeScript 타입 감각을 그대로 유지한 채, 이제 실제 런타임 입력을 받아들이는 쪽으로 한 걸음 나간다. 이 프로젝트가 다루는 건 거대한 서버가 아니라 아주 작은 CLI지만, 파일 경로, NDJSON, 환경 변수, 출력 포맷, 오류 메시지 같은 현실적인 입력 표면이 이미 다 들어 있다.

## 1. 출발점은 "Node API를 써 본다"가 아니라 런타임 입력을 의심하는 습관이었다

문제 정의는 파일과 환경 변수에 의존하는 작은 CLI를 만들며 Node.js 런타임을 익히라고 하지만, 소스가 보여 주는 핵심은 훨씬 선명하다. 입력 파일은 언제든 없을 수 있고, 줄 중 하나는 깨진 JSON일 수 있으며, env 값은 문서와 다르게 들어올 수 있다. 이 프로젝트는 바로 그런 입력을 어디서 믿지 않기로 할지 연습하는 bridge다.

`docs/concepts/streaming-cli.md`도 같은 메시지를 준다. 로그 파일을 처리하는 CLI는 "작동한다"보다 "실패를 설명한다"가 더 중요하다고 말한다.

## 2. parser는 파일을 한 번에 읽지 않고 줄 단위로 신뢰를 쌓는다

`request-report.ts`의 `readRequestLog()`가 이 프로젝트의 첫 전환점이다.

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

여기서 중요한 건 단순한 메모리 절약이 아니다. 입력을 줄 단위로 따라가면서, 깨진 JSON이 생기면 정확히 몇 번째 줄에서 문제가 났는지 설명할 수 있게 만드는 점이 더 중요하다.

```ts
throw new Error(`Invalid JSON at line ${lineNumber}: ${message}`);
```

이 한 줄 때문에 이 도구는 "파일이 이상함"에서 멈추지 않고, 어디를 다시 봐야 하는지까지 알려 주는 쪽으로 바뀐다.

## 3. 요약 단계에서 이 도구가 어떤 운영 숫자를 중요하게 보는지가 결정된다

파서를 만든 뒤 바로 나오는 선택은 `summarizeRequests()`다. 이 함수는 단순 집계처럼 보이지만, 사실상 "무엇을 보고서로 볼 것인가"를 정한다.

```ts
for (const record of records) {
  uniqueUsers.add(record.userId);
  perRoute[record.route] = (perRoute[record.route] ?? 0) + 1;

  if (record.status >= 400) {
    errorCount += 1;
  }
}
```

이 프로젝트가 남기는 숫자는 네 가지다.
- 전체 요청 수
- 고유 사용자 수
- 에러 수
- route별 요청 수

즉 이 도구는 raw log viewer가 아니라, 아주 작은 운영 보고서 generator에 가깝다. 샘플 fixture가 `5 requests / 3 users / 2 errors`로 고정되는 것도 바로 이 선택 덕분이다.

## 4. 출력 포맷은 데이터 가공이 아니라 독자를 고르는 결정이 된다

`formatSummary()`는 같은 summary를 text와 JSON 두 표면으로 보여 준다.

```ts
export function formatSummary(summary: RequestSummary, format: "text" | "json"): string {
  if (format === "json") {
    return JSON.stringify(summary, null, 2);
  }
  // ...
}
```

text는 사람이 터미널에서 바로 읽기 좋고, JSON은 다른 도구가 파이프라인에 바로 연결하기 좋다. 이 작은 선택이 이후 API 응답, 배치 리포트, 운영 스크립트 출력 설계의 감각으로 이어진다.

## 5. CLI는 env와 argv를 검증하는 마지막 런타임 경계가 된다

`runCli()`는 이 프로젝트를 유틸리티 함수 묶음에서 실제 도구로 바꾸는 지점이다.

```ts
const requestedFormat = env.REPORT_FORMAT ?? "text";
if (requestedFormat !== "text" && requestedFormat !== "json") {
  stderr.write("REPORT_FORMAT must be either text or json\n");
  return 1;
}
```

여기서 보이는 핵심은 허용값을 문서가 아니라 코드에서 직접 닫는다는 점이다. `REPORT_FORMAT=yaml` 같은 애매한 상태는 즉시 stderr와 non-zero exit code로 정리된다. 파일 경로가 없을 때도 마찬가지다.

다만 이번 재실행에서 중요한 불일치가 하나 드러났다. 구현은 `args[0]`을 파일 경로로 기대하는데, README와 문제 스크립트는 `pnpm start -- <path>`를 사용 예로 제시한다. 실제로 이 명령은 `--` 자체가 첫 번째 인자로 들어가면서 `ENOENT ... /node/--`로 실패한다. 즉 구현은 건강하지만, 권장 재현 경로는 현재 CLI와 맞지 않는다.

## 6. 테스트는 성공 숫자와 실패 표면을 함께 고정한다

`node/tests/request-report.test.ts`는 다섯 개 테스트로 이 프로젝트의 중심을 묶는다.
- fixture 파일 읽기
- summary 숫자 검증
- text report formatting
- `REPORT_FORMAT=json` 성공
- invalid format 실패

이 테스트 덕분에 이 프로젝트는 "대충 잘 읽히는 듯하다"가 아니라, 정확히 어떤 숫자와 어떤 오류 메시지를 돌려줘야 하는지 계약이 생긴다.

## 7. 이번 재실행은 구현과 재현 문서가 갈라지는 지점을 분명히 보여 줬다

이번 턴에서 실제로 확인한 결과는 이렇다.

```bash
pnpm run build
pnpm run test
REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson
node dist/cli.js ../problem/data/request-log.ndjson
REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson
bash problem/script/run-example.sh
```

결과는 두 갈래였다.
- 워크스페이스 자체
  `build` 통과, `test` 통과, direct `node dist/cli.js` 실행도 text/json 모두 정상
- 권장 재현 표면
  `pnpm start -- ...`는 `--`를 파일 경로로 읽어 실패
  `run-example.sh`는 상위 폴더에서 `package.json`을 찾지 못하고, `node/` 안에서 실행해도 같은 `--` 문제로 실패

즉 이 프로젝트의 진짜 교훈은 "CLI가 동작한다"와 "문서가 권하는 실행 방법이 동작한다"가 별개의 검증 대상이라는 점이다.

## 정리

이 프로젝트는 `backend-node` 트랙에서 파일, env, stream, 출력 포맷 같은 현실적인 입력을 처음 정면으로 다룬다. line-oriented parser와 summary shape, env validation 자체도 중요하지만, 이번 Todo에서 더 또렷해진 건 재현 문서와 실제 CLI 계약을 끝까지 맞춰 봐야 한다는 사실이다. 그 감각이 다음 장에서 HTTP request/response 표면으로 이어진다.

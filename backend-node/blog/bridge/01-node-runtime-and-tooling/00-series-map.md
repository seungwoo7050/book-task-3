# 01-node-runtime-and-tooling

이 글은 `00-language-and-typescript`에서 메모리 안의 값을 정리하던 감각을, 실제 파일과 env와 CLI 표면으로 끌고 나오는 첫 Node 런타임 프로젝트로 읽는다. 중요한 건 Node API를 많이 쓰는 것이 아니라, 런타임 입력을 어디서 검증하고 어떤 메시지로 실패를 닫을지 정하는 일이다.

## 이 Todo가 붙잡는 질문
디스크의 NDJSON 로그와 환경 변수 같은 믿을 수 없는 런타임 입력을, 작은 CLI 안에서 어디까지 안전하게 읽고 어떤 보고 형식으로 고정할 것인가?

문제 정의도 이 축을 분명히 잡고 있다. 목표는 파일과 환경 변수에 의존하는 작은 CLI를 만들며 Node.js 런타임과 도구 체인을 익히는 것이다. 그래서 이 프로젝트의 중심은 `readline` 자체보다, line-oriented parser, 요약 지표 선택, `REPORT_FORMAT`, 경로 오류 메시지다.

## 먼저 잡아둘 범위
- `node/src/request-report.ts`
  NDJSON를 줄 단위로 읽고 `totalRequests`, `uniqueUsers`, `errorCount`, `perRoute` 요약을 만든다.
- `node/src/cli.ts`
  파일 경로와 `REPORT_FORMAT`을 받아 text/json 출력으로 닫는다.
- `node/tests/request-report.test.ts`
  fixture 기반 요약 숫자와 CLI 실패 조건을 고정한다.
- `problem/data/request-log.ndjson`
  실제 요약 결과가 왜 `5 requests / 3 users / 2 errors`인지 설명하는 샘플 입력이다.

이 프로젝트의 핵심은 "로그를 읽는다"보다 "입력 계약을 어디서 선명하게 만드는가"다. `readRequestLog()`는 경로를 `path.resolve()`로 고정하고, JSON 파싱 실패를 줄 번호가 포함된 오류로 바꾼다. `runCli()`는 env 허용값을 `text | json`으로 제한한다. 이런 작은 선택들이 이후 운영 스크립트나 ETL 도구의 감각으로 이어진다.

## 이번 글에서 따라갈 순서
1. 왜 이 프로젝트가 단순 Node API 연습이 아니라 런타임 입력 계약의 시작점인지 본다.
2. stream + `readline`으로 NDJSON를 line-oriented하게 읽는 이유를 본다.
3. 요약 지표를 `route / user / error` 중심으로 고른 이유를 본다.
4. `REPORT_FORMAT`와 파일 경로 검증이 CLI 표면을 어떻게 닫는지 본다.
5. 실제 재검증에서 무엇은 동작했고 무엇은 README/스크립트와 어긋났는지 함께 닫는다.

## 가장 중요한 코드 신호
- `node/src/request-report.ts`
  파일 입력, line number 포함 에러, summary shape를 모두 만든다.
- `node/src/cli.ts`
  env와 argv가 실제 런타임 계약으로 바뀌는 지점이다.
- `node/tests/request-report.test.ts`
  fixture 숫자와 invalid format 처리를 고정한다.
- `docs/concepts/streaming-cli.md`
  "작동한다보다 실패를 설명한다"라는 이 프로젝트의 기준을 짧게 요약한다.

## 이번 턴의 재검증 메모
- `pnpm run build`: 통과
- `pnpm run test`: 통과, `5`개 테스트 전부 성공
- `REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson`: 정상 출력
- `node dist/cli.js ../problem/data/request-log.ndjson`: 정상 text 출력
- `REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson`: 실패, `--`를 파일 경로로 읽어 `ENOENT`
- `bash problem/script/run-example.sh`: 상위 폴더에서는 `No package.json`, `node/` 안에서는 같은 `--` 인자 문제로 실패

즉 구현 자체는 건강하지만, README와 문제 스크립트가 권하는 `pnpm start -- ...` 재현 경로는 현재 CLI 계약과 맞지 않는다. 이 차이를 분리해서 읽는 것이 이번 Todo의 핵심이다.

## 다 읽고 나면 남는 것
- 왜 이 프로젝트가 "파일 읽기 예제"가 아니라 런타임 입력을 다루는 최소 운영 도구의 시작점인지 설명할 수 있다.
- line-oriented parsing, summary shape, env validation이 각각 어떤 역할을 하는지 분리해서 볼 수 있다.
- 다음 `02-http-and-api-basics`에서 왜 파일 입력 감각이 HTTP request/response 감각으로 이어지는지 자연스럽게 연결된다.

# 01-node-runtime-and-tooling series map

`01-node-runtime-and-tooling`은 TypeScript 타입 연습을 실제 Node 런타임 입출력으로 옮기는 첫 단계다. 그래서 이 시리즈는 "로그 파일을 어떻게 읽고, 어떤 summary shape로 바꾸고, 그 결과를 어떤 CLI contract로 노출했는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 [`node/src/request-report.ts`](../../../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/src/request-report.ts)에서 stream parser와 summarizer가 붙는 순서로 복원한다.
- 검증은 [`node/tests/request-report.test.ts`](../../../study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/tests/request-report.test.ts)와 `problem/data/request-log.ndjson` 실제 출력으로 닫는다.
- CLI 예시는 `pnpm start -- ...`보다 검증이 선명한 `node dist/cli.js ...`를 기준으로 남긴다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ REPORT_FORMAT=json node dist/cli.js ../problem/data/request-log.ndjson
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   스트림 파싱, summary model, CLI/env 처리가 어떤 순서로 붙었는지 따라간다.

# 01-node-runtime-and-tooling structure plan

## 중심 질문

- Node 런타임에서 파일 스트림과 라인 단위 파싱을 어디까지 직접 다뤘는가
- summary shape를 먼저 고정한 뒤 formatter를 붙인 이유는 무엇인가
- CLI와 env가 붙는 순간 어떤 runtime edge가 새로 드러났는가

## 10-development-timeline.md

- 오프닝: 이 프로젝트가 "파일, env, stdout/stderr를 직접 만지는 첫 런타임 브리지"라는 점을 분명히 한다.
- Phase 1: `readRequestLog()`에서 `stat`, `createReadStream`, `readline`을 묶어 NDJSON line parser를 만든 장면.
- Phase 2: `summarizeRequests()`와 `formatSummary()`로 출력 전에 summary model을 고정한 장면.
- Phase 3: `runCli()`와 테스트가 env 기반 formatter, 잘못된 인자, 실제 fixture 실행을 닫는 장면.
- 강조 포인트: README의 `pnpm start -- <path>`보다 빌드 산출물 `node dist/cli.js`를 직접 호출했을 때 실제 검증이 더 명확하게 드러났다는 점.

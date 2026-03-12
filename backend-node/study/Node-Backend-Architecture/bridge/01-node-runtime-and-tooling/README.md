# 01-node-runtime-and-tooling

- 그룹: `Bridge`
- 상태: `verified`
- 공개 답안 레인: `node/`
- 성격: 신규 설계

## 한 줄 문제

Node.js 런타임에서 파일, env, stream, scripts를 직접 다루며 작은 운영성 감각을 익히는 런타임 브리지 문제다.

## 성공 기준

- `process.env`, `fs`, `path`, stream을 사용해 CLI 입력과 파일 처리를 연결할 수 있다.
- NDJSON 로그처럼 줄 단위 데이터를 안전하게 읽고 요약할 수 있다.
- 빌드, 테스트, 실행 스크립트를 워크스페이스 단위로 재현할 수 있다.

## 내가 만든 답

- `node/`에 NDJSON 요청 로그를 요약하는 CLI와 테스트를 구성했다.
- 파일 경로, 출력 포맷, JSON 파싱 실패를 명시적으로 다루도록 설계했다.
- 후속 HTTP/API 프로젝트에서 필요한 런타임 입출력 감각을 여기서 먼저 고정했다.

## 제공 자료

- `problem/README.md`
- `node/`
- `docs/`
- `notion/`

## 실행과 검증

### Node 구현
- 작업 디렉터리: `node/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test`
- run: `REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson`

## 왜 다음 단계로 이어지는가

- `02-http-and-api-basics`에서 같은 런타임 감각을 HTTP 요청/응답 모델로 옮긴다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [node/README.md](node/README.md)에서 확인한다.

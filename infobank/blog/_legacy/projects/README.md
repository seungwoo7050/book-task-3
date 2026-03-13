# infobank projects blog

`blog/projects/`는 두 인포뱅크 과제를 project-level source-first 시리즈로 다시 읽는 인덱스다. 문체는 blog지만, 근거는 현재 `projects/*` 소스와 테스트만 사용한다.

## 프로젝트 카탈로그

| 프로젝트 | 시리즈 입구 | 원 프로젝트 | 대표 검증 신호 |
| --- | --- | --- | --- |
| `01 MCP 추천 최적화` | [`01-mcp-recommendation-demo/README.md`](01-mcp-recommendation-demo/README.md) | [`../../projects/01-mcp-recommendation-demo/README.md`](../../projects/01-mcp-recommendation-demo/README.md) | `pnpm seed` -> `Seeded 12 catalog entries...`, `pnpm test` -> `9 passed`, `pnpm release:gate rc-release-check-bot-1-5-0` -> `"passed": true` |
| `02 챗봇 상담 품질 관리` | [`02-chat-qa-ops/README.md`](02-chat-qa-ops/README.md) | [`../../projects/02-chat-qa-ops/README.md`](../../projects/02-chat-qa-ops/README.md) | `make gate-all` -> `MP1~MP5 + frontend tests passed`, `make smoke-postgres` -> `PostgreSQL smoke verification passed` |

## 공통 메모

- 두 시리즈 모두 `notion/`과 `notion-archive/`를 읽지 않는다.
- chronology는 과거 timestamp를 꾸며내지 않고 `Day / Session`으로 적는다.
- 세션 경계는 README와 테스트가 보여 주는 `v0 -> v1 -> v2 -> v3` 버전 사다리로 맞춘다.
- legacy redirect 경로는 설명 대상으로만 다루고, source set에는 넣지 않는다.

## 읽는 순서

1. `01-mcp-recommendation-demo`로 catalog, recommendation, release gate 흐름을 먼저 읽는다.
2. `02-chat-qa-ops`로 rubric, evaluation, regression, self-hosted job 흐름을 이어서 읽는다.
3. 실제 제품 표면이 더 필요하면 각 blog 시리즈에서 원 프로젝트 README로 내려간다.

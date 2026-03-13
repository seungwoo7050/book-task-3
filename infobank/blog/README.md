# infobank blog

`infobank/blog/`는 두 인포뱅크 프로젝트를 "무엇을 만들었는가"보다 "어떻게 여기까지 왔는가" 중심으로 다시 읽는 레이어다. 최종 결과물만 보는 대신, 설계가 어디서 갈렸고 어떤 검증을 거쳐 지금 형태가 되었는지 차례대로 따라가게 만드는 것이 이 디렉터리의 목적이다.

이 버전은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 직전 시리즈는 [`_legacy/2026-03-13-isolate-and-rewrite/`](./_legacy/2026-03-13-isolate-and-rewrite/)에 보관했고, 이번 글에서는 예전 blog를 입력 근거로 사용하지 않았다. 근거는 `projects/*` 아래의 소스코드, `README.md`, `problem/`, `docs/`, 테스트, 실제 CLI 재실행 결과만 사용했다.

## 여기서 다루는 독립 프로젝트

이번 Batch Mode에서 실제로 처리한 독립 프로젝트는 `projects/*` 아래 두 개다.

- `projects/01-mcp-recommendation-demo`: MCP 추천 시스템이 catalog 계약, 추천 로직, release gate, self-hosted 운영 표면까지 어떻게 확장됐는지 끝까지 보여 준다.
- `projects/02-chat-qa-ops`: 챗봇 품질 평가가 rule/evidence/judge 파이프라인에서 시작해 regression proof와 self-hosted review ops로 어떻게 자랐는지 보여 준다.

반대로 `mcp-recommendation-demo/`, `chat-qa-ops/`는 pre-migration redirect만 남은 경로라 입력 프로젝트에서 제외했다. `docs/`, `.github/`, `blog/`, `projects/` 루트는 공용 문서나 인덱스 레이어라 독립 프로젝트로 보지 않았다.

## 지금 읽을 수 있는 시리즈

| 프로젝트 | 시리즈 입구 | 이 시리즈가 보여 주는 것 | 대표 검증 신호 |
| --- | --- | --- | --- |
| `01 MCP 추천 최적화` | [`projects/01-mcp-recommendation-demo/README.md`](./projects/01-mcp-recommendation-demo/README.md) | catalog contract에서 시작한 추천 시스템이 compare, release gate, operator UI까지 연결되는 흐름 | `Seeded 12 catalog entries...`, `top3Recall 0.9583`, `release gate passed: true`, `v3 tests 8 passed \| 2 skipped` |
| `02 챗봇 상담 품질 관리` | [`projects/02-chat-qa-ops/README.md`](./projects/02-chat-qa-ops/README.md) | 상담 품질 평가가 golden regression과 self-hosted review surface로 이어지는 흐름 | `gate-all: 3+5+15+5+16 passed`, `PostgreSQL smoke verification passed`, `84.06 -> 87.76`, `v3 gate-all passed` |

## 읽는 순서

1. 루트 [`../README.md`](../README.md)에서 두 과제의 공식 답과 확장 답을 먼저 확인한다.
2. [`projects/README.md`](./projects/README.md)에서 원하는 프로젝트의 시리즈 입구를 고른다.
3. 각 프로젝트의 `README.md`와 `00-series-map.md`로 전체 흐름과 읽는 기준을 잡는다.
4. `_evidence-ledger.md`에서 이 시리즈가 어떤 근거로 복원됐는지 확인한다.
5. `10 -> 20 -> 30` 문서 순서로 구현, 검증, productization 흐름을 따라간다.

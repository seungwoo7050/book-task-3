# infobank projects blog

`blog/projects/`는 `infobank/projects/*` 아래의 독립 프로젝트를 하나씩 다시 읽는 카탈로그다. 이번 리라이트에서는 기존 project blog를 [`../_legacy/2026-03-13-isolate-and-rewrite/projects/`](../_legacy/2026-03-13-isolate-and-rewrite/projects/)로 옮긴 뒤, 현재 소스와 CLI 결과만으로 새 시리즈를 다시 썼다.

## 프로젝트 카탈로그

| 프로젝트 | 시리즈 입구 | supporting doc | 원 프로젝트 |
| --- | --- | --- | --- |
| `01 MCP 추천 최적화` | [`01-mcp-recommendation-demo/README.md`](./01-mcp-recommendation-demo/README.md) | [`_evidence-ledger.md`](./01-mcp-recommendation-demo/_evidence-ledger.md), [`_structure-outline.md`](./01-mcp-recommendation-demo/_structure-outline.md) | [`../../projects/01-mcp-recommendation-demo/README.md`](../../projects/01-mcp-recommendation-demo/README.md) |
| `02 챗봇 상담 품질 관리` | [`02-chat-qa-ops/README.md`](./02-chat-qa-ops/README.md) | [`_evidence-ledger.md`](./02-chat-qa-ops/_evidence-ledger.md), [`_structure-outline.md`](./02-chat-qa-ops/_structure-outline.md) | [`../../projects/02-chat-qa-ops/README.md`](../../projects/02-chat-qa-ops/README.md) |

## 이 레이어를 읽는 방법

- 각 시리즈는 `00-series-map.md`에서 전체 질문을 먼저 제시한다.
- `_evidence-ledger.md`는 이 글이 어떤 코드와 CLI를 근거로 썼는지 보여 주는 복원 기록이다.
- `_structure-outline.md`는 시리즈를 왜 `10`, `20`, `30`으로 나눴는지 설명한다.
- 최종 공개 글은 언제나 `10 -> 20 -> 30` 순서로 읽으면 된다.

## 공통 원칙

- 근거는 현재 `projects/*`의 소스, `README.md`, `docs/`, 테스트, 실제 CLI 결과만 사용한다.
- `notion/`, `notion-archive/`, 예전 `blog/` 초안은 입력 근거에서 제외한다.
- chronology는 세밀한 시간보다 `Stage`, `Version`, `검증 결과`를 중심으로 복원한다.

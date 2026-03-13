# infobank projects blog

`blog/projects/`는 두 인포뱅크 과제를 독립 프로젝트 단위로 다시 읽는 catalog다. chronology는 모두 현재 `projects/*` 소스와 테스트에서 복원했고, legacy blog 초안은 [`../_legacy/projects/`](../_legacy/projects/)로 격리했다.

## 프로젝트 카탈로그

| 프로젝트 | 시리즈 입구 | evidence ledger | 원 프로젝트 | 대표 검증 신호 |
| --- | --- | --- | --- | --- |
| `01 MCP 추천 최적화` | [`01-mcp-recommendation-demo/README.md`](01-mcp-recommendation-demo/README.md) | [`01-mcp-recommendation-demo/_evidence-ledger.md`](01-mcp-recommendation-demo/_evidence-ledger.md) | [`../../projects/01-mcp-recommendation-demo/README.md`](../../projects/01-mcp-recommendation-demo/README.md) | `Seeded 12 catalog entries...`, `top3Recall 0.9583`, `release gate passed: true`, `artifact export generated` |
| `02 챗봇 상담 품질 관리` | [`02-chat-qa-ops/README.md`](02-chat-qa-ops/README.md) | [`02-chat-qa-ops/_evidence-ledger.md`](02-chat-qa-ops/_evidence-ledger.md) | [`../../projects/02-chat-qa-ops/README.md`](../../projects/02-chat-qa-ops/README.md) | `gate-all passed`, `PostgreSQL smoke verification passed`, `improvement-report 84.06 -> 87.76`, `v3 gate-all passed` |

## 공통 메모

- supporting doc은 `_evidence-ledger.md`, `_structure-outline.md` 두 개로 고정한다.
- 공개 시리즈의 읽기 순서는 각 프로젝트 `00-series-map.md` 다음에 `10`, `20`, `30` 문서를 따르는 구조다.
- `git log -- projects/...`가 migration commit 하나만 보여 주기 때문에, 버전 ladder와 README 검증 명령이 chronology의 주된 시간 표지 역할을 한다.

# infobank blog

`blog/`는 `infobank/`의 source-first reconstructed timeline layer다. 이 디렉터리는 기존 `README.md`, `problem/`, `docs/`, `capstone/`을 대체하지 않고, 두 과제를 `v0 -> v1 -> v2 -> v3` 버전 사다리와 실제 검증 명령으로 다시 읽기 위한 project-level 시리즈만 보관한다.

기존 초안은 [`_legacy/`](./_legacy/)로 격리했다. 새 시리즈는 그 글을 입력 근거로 삼지 않고, 현재 `projects/*` 소스, README, docs, 테스트, CLI 재실행 결과만 사용한다.

## 이 레이어의 기준

- 적용 단위는 `projects/*` 아래의 독립 프로젝트다.
- 기본 원천은 `README.md`, `problem/README.md`, `docs/stage-catalog.md`, `docs/verification-matrix.md`, `capstone/*/README.md`, 실제 구현 코드, 테스트, runbook, `docker-compose.yml`, `Makefile`, `package.json`, `pyproject.toml`, `git log -- projects/...`다.
- `notion/`과 `notion-archive/`는 읽지 않는다.
- legacy redirect인 `mcp-recommendation-demo/`, `chat-qa-ops/`는 source set에 포함하지 않는다.
- chronology는 세밀한 시각 대신 `Day / Session` 형식을 기본으로 쓴다.
- supporting doc인 `_evidence-ledger.md`와 `_structure-outline.md`는 근거와 설계 기록이고, 최종 읽기 순서는 항상 `00 -> 10 -> 20 -> 30`이다.

## 현재 범위

| 프로젝트 | blog 입구 | 원 프로젝트 | 대표 검증 신호 |
| --- | --- | --- | --- |
| `01 MCP 추천 최적화` | [`projects/01-mcp-recommendation-demo/README.md`](projects/01-mcp-recommendation-demo/README.md) | [`../projects/01-mcp-recommendation-demo/README.md`](../projects/01-mcp-recommendation-demo/README.md) | `Seeded 12 catalog entries...`, `9 passed`, `release gate passed: true`, `v3 test: 8 passed \| 2 skipped` |
| `02 챗봇 상담 품질 관리` | [`projects/02-chat-qa-ops/README.md`](projects/02-chat-qa-ops/README.md) | [`../projects/02-chat-qa-ops/README.md`](../projects/02-chat-qa-ops/README.md) | `gate-all: 3+5+15+5+16 passed`, `PostgreSQL smoke verification passed`, `v3 gate-all passed` |

## 읽는 순서

1. 루트 [`../README.md`](../README.md)에서 공식 답과 확장 답의 위치를 먼저 확인한다.
2. [`projects/README.md`](projects/README.md)에서 원하는 과제의 blog 시리즈 입구를 고른다.
3. 각 프로젝트 `README.md`에서 source set, supporting doc, 검증 진입점을 확인한다.
4. `00-series-map.md`로 문제 경계와 버전 사다리를 고정한다.
5. `10`, `20`, `30` 문서에서 실제 구현 순서와 검증 신호를 따라간다.

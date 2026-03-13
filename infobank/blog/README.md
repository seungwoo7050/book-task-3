# infobank blog

`blog/`는 `infobank/`의 공개 blog layer다. 이 디렉터리는 기존 `README.md`, `docs/`, `problem/`, `capstone/`을 대체하지 않고, 두 과제를 `source-first reconstructed timeline`으로 다시 읽기 위한 긴 학습 로그만 모아 둔다.

## 이 레이어의 기준

- 적용 단위는 `projects/*` 아래의 독립 프로젝트다.
- 기본 원천은 `README.md`, `problem/README.md`, `capstone/*/README.md`, 실제 구현 코드, 테스트, runbook, `docker-compose.yml`, `Makefile`, `package.json`, `pyproject.toml`, `git log -- projects/...`다.
- `notion/`과 `notion-archive/`는 읽지 않는다.
- 현재 구조의 source of truth는 `projects/01-mcp-recommendation-demo`와 `projects/02-chat-qa-ops`다. legacy redirect인 `mcp-recommendation-demo/`, `chat-qa-ops/`는 source set에 포함하지 않는다.
- chronology는 세밀한 시각 대신 `Day / Session` 형식을 기본으로 쓴다.
- 세션 경계는 현재 소스가 보여 주는 버전 사다리 `v0 -> v1 -> v2 -> v3`로 고정한다.
- 코드는 판단이 갈린 짧은 조각만 inline으로 남기고, CLI는 세션별 전체 재현 경로를 묶어 적는다.

## 현재 범위

| 프로젝트 | blog 입구 | 원 프로젝트 | 대표 검증 신호 |
| --- | --- | --- | --- |
| `01 MCP 추천 최적화` | [`projects/01-mcp-recommendation-demo/README.md`](projects/01-mcp-recommendation-demo/README.md) | [`../projects/01-mcp-recommendation-demo/README.md`](../projects/01-mcp-recommendation-demo/README.md) | `Seeded 12 catalog entries`, `9 passed`, `release gate passed: true` |
| `02 챗봇 상담 품질 관리` | [`projects/02-chat-qa-ops/README.md`](projects/02-chat-qa-ops/README.md) | [`../projects/02-chat-qa-ops/README.md`](../projects/02-chat-qa-ops/README.md) | `gate-all passed`, `PostgreSQL smoke verification passed` |

## 읽는 순서

1. 루트 [`../README.md`](../README.md)에서 공식 답과 확장 답의 위치를 먼저 확인한다.
2. [`projects/README.md`](projects/README.md)에서 원하는 과제의 blog 시리즈 입구를 고른다.
3. 각 프로젝트의 `README.md`에서 source set과 검증 진입점을 확인한다.
4. `00-series-map.md`로 문제 경계와 실제 구현 표면을 고정한다.
5. `10-development-timeline.md`에서 버전 사다리를 chronology로 따라간다.

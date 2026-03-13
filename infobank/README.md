# Infobank 과제 학습 아카이브

이 저장소는 인포뱅크 과제를 `문제 -> 공식 제출 답 -> 확장 답 -> 검증 -> 학습 기록` 순서로 읽히게 다시 고정한 study-first 레포다. 커리큘럼 설명은 뒤로 보내고, GitHub 첫 화면에서 각 과제가 무엇을 묻고 어떤 버전을 공식 답으로 삼는지부터 바로 찾게 만든다.

## Capstone First

| 과제 | 문제 한 줄 | 공식 답 (`v2`) | 확장 답 (`v3`) | canonical verify | 시작 위치 |
| --- | --- | --- | --- | --- | --- |
| 1번 `MCP 추천 최적화` | catalog, selector, compare, release gate를 갖춘 추천 시스템을 어떻게 설계하고 증명할까? | [`projects/01-mcp-recommendation-demo/capstone/v2-submission-polish`](./projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/README.md) | [`projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening`](./projects/01-mcp-recommendation-demo/capstone/v3-oss-hardening/README.md) | `pnpm db:up`, `pnpm migrate`, `pnpm seed`, `pnpm test`, `pnpm eval`, `pnpm compatibility rc-release-check-bot-1-5-0`, `pnpm release:gate rc-release-check-bot-1-5-0` | [`projects/01-mcp-recommendation-demo`](./projects/01-mcp-recommendation-demo/README.md) |
| 2번 `챗봇 상담 품질 관리` | rubric, guardrail, evidence, regression, dashboard를 갖춘 QA Ops 계층을 어떻게 만들까? | [`projects/02-chat-qa-ops/capstone/v2-submission-polish`](./projects/02-chat-qa-ops/capstone/v2-submission-polish/README.md) | [`projects/02-chat-qa-ops/capstone/v3-self-hosted-oss`](./projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/README.md) | `UV_PYTHON=python3.12 uv sync --extra dev`, `UV_PYTHON=python3.12 make gate-all`, `UV_PYTHON=python3.12 make smoke-postgres` | [`projects/02-chat-qa-ops`](./projects/02-chat-qa-ops/README.md) |

## 구조

```text
infobank/
├── blog/
│   └── projects/
├── projects/
│   ├── 01-mcp-recommendation-demo/
│   │   ├── problem/
│   │   ├── docs/
│   │   ├── stages/
│   │   └── capstone/
│   └── 02-chat-qa-ops/
│       ├── problem/
│       ├── docs/
│       ├── stages/
│       └── capstone/
├── docs/
│   ├── catalog/
│   ├── curriculum/
│   └── policies/
└── .github/
```

## 지금 읽는 순서

1. [`projects/README.md`](./projects/README.md)에서 두 과제의 공식 답과 확장 답을 먼저 고른다.
2. 선택한 프로젝트의 `problem/README.md`에서 원문 문제와 이 레포의 답 범위를 확인한다.
3. 바로 결과물을 보려면 `capstone/v2-submission-polish`부터 읽고, 제품화 방향이 궁금하면 `capstone/v3-*`로 이어진다.
4. 그 답이 어떤 학습 단위에서 올라왔는지 알고 싶으면 `stages/00~07`과 각 `notion/05-development-timeline.md`를 거꾸로 읽는다.

## 공용 문서

- [`docs/README.md`](./docs/README.md): 전역 문서 인덱스
- [`blog/README.md`](./blog/README.md): `notion/` 없이 현재 소스와 테스트만으로 다시 읽은 source-first blog index
- [`docs/catalog/path-migration-map.md`](./docs/catalog/path-migration-map.md): 이전 경로와 새 경로 대응표
- [`docs/curriculum/project-selection-rationale.md`](./docs/curriculum/project-selection-rationale.md): 왜 두 과제를 이렇게 재구성했는지
- [`docs/curriculum/curriculum-map.md`](./docs/curriculum/curriculum-map.md): stage와 capstone 전체 맵
- [`docs/policies/readme-contract.md`](./docs/policies/readme-contract.md): README가 답해야 하는 질문
- [`docs/policies/code-comment-language.md`](./docs/policies/code-comment-language.md): 한글 주석/docstring 규칙

## 문서 원칙

- 설명 문서는 한글 우선으로 쓴다.
- `README.md`, `problem/README.md`, `docs/README.md`는 front door 문서다.
- `notion/`은 현재 판단 과정과 재현 경로를 남기는 공개 노트다.
- `notion-archive/`는 pre-migration 경로 기준 기록을 보존하는 역사 문서다.
- 구현하지 않았거나 검증하지 않은 범위는 `planned`로 분리해 적는다.

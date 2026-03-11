> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Source Brief — 문제 정의

## 풀어야 하는 문제

MCP(Model Context Protocol)는 LLM 도구 호출을 위한 표준이다.
도구가 많아지면 **어떤 도구를 추천할 것인가**라는 문제가 생긴다.

이 프로젝트의 목표는:
1. MCP 도구 카탈로그를 관리하고
2. 사용자 요청에 맞는 도구를 추천하고
3. 추천 품질을 측정/개선하는 시스템을 만드는 것이다.

## 왜 MCP 추천인가

MCP 생태계가 커지면서 도구 선택이 점점 어려워진다.
GitHub repo inspector, PostgreSQL schema mapper, Korean docs search 등
10개 이상의 도구 중에서 현재 맥락에 맞는 것을 골라야 한다.

단순 키워드 매칭으로는 안 된다. "릴리즈 체크를 해야 하는데"라는 요청에
release-check-bot과 github-repo-inspector가 동시에 걸릴 수 있다.
**근거 있는 선택**이 필요하다.

## capstone 목표

v0에서 baseline selector로 시작해서,
v2에서 compatibility gate + release gate까지 완성하는 것.
v3에서는 이걸 self-hosted OSS로 패키징한다.

## reference spine

프로젝트 전체를 관통하는 참조 문서:
- `docs/reference-spine.md` — 추천 시스템 참조 구조
- `docs/project-selection-rationale.md` — 이 주제를 선택한 이유
- `shared/src/catalog.ts` — 10+ MCP 도구 카탈로그
- `shared/src/eval.ts` — offline eval case

## 제약

- 실제 MCP 서버 연동은 범위 밖. seed 데이터로 동작을 증명한다.
- LLM 기반 추천은 사용하지 않는다. 규칙과 가중치 기반으로 구현한다.

# 01 MCP 추천 최적화 문제 정의

## 원래 과제가 묻는 것

- MCP 추천 품질을 어떻게 설명 가능한 구조로 만들 것인가
- metadata schema, selector, compare, release 판단을 어떤 기준으로 묶을 것인가
- 사용자가 한국어로 추천 이유를 이해하고, 운영자가 실험 결과를 재현할 수 있게 만들 수 있는가

## 이 레포의 공식 답

- 공식 답은 `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish`다.
- 이 버전은 submission 기준으로 필요한 추천 로직, compare, quality gate, artifact export까지 포함한다.
- `stages/00~07`은 공식 답을 이루는 개념과 증빙 단위를 잘게 쪼갠 학습 pack이다.

## 제공 자료와 기준

- 전역 커리큘럼 근거: `docs/curriculum/project-selection-rationale.md`
- 전역 순서표: `docs/curriculum/curriculum-map.md`
- 레퍼런스 뼈대: `docs/curriculum/reference-spine.md`

## 범위 밖

- production SaaS 운영
- multi-tenant 조직 관리
- 실제 외부 MCP registry와의 장기 운영 보증

## canonical verify

```bash
cd projects/01-mcp-recommendation-demo/capstone/v2-submission-polish
pnpm install --no-frozen-lockfile
pnpm db:up
pnpm migrate
pnpm seed
pnpm test
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
```

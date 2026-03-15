# infobank 비필수 문제지

여기서 `elective`는 중요하지 않다는 뜻이 아니라, 공식 제출 답 직전의 baseline과 hardening 버전을 따로 읽는 확장 문제라는 뜻입니다. 핵심 vocabulary를 익힌 뒤, "어디까지가 baseline이고 어디서부터 hardening인가"를 구분하는 항목만 남깁니다.

## 01-mcp-recommendation-demo

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [v0-initial-demo-python](v0-initial-demo-python.md) | 처음 보는 사람도 로컬에서 바로 실행해 볼 수 있는 상담 품질 QA Ops baseline을 만든다. 품질 평가 파이프라인과 운영 UI를 한 번 끝까지 연결해 보는 것이 핵심이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v0-initial-demo/python && python3 -m pytest` |
| [v0-initial-demo-react](v0-initial-demo-react.md) | 시작 위치의 구현을 완성해 registry seed와 manifest validation, baseline selector와 한국어 추천 근거, offline eval과 기본 운영 화면을 한 흐름으로 설명하고 검증한다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e` |
| [v1-ranking-hardening-react](v1-ranking-hardening-react.md) | 시작 위치의 구현을 완성해 reranker와 compare runner, usage/feedback/experiment API, 운영 콘솔의 compare 화면을 한 흐름으로 설명하고 검증한다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e` |
| [v1-regression-hardening-python](v1-regression-hardening-python.md) | v0를 바탕으로 회귀 안정성과 lineage를 강화해, 개선 실험이 실제로 나아졌는지 비교 가능한 상태를 만든다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/python && python3 -m pytest` |
| [v1-regression-hardening-react](v1-regression-hardening-react.md) | v0를 바탕으로 회귀 안정성과 lineage를 강화해, 개선 실험이 실제로 나아졌는지 비교 가능한 상태를 만든다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.

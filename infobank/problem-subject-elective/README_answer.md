# infobank 비필수 답안지

이 문서는 공식 제출 답 직전의 baseline과 hardening 버전을 source-first로 해설하는 답안지다. 각 항목은 "최소 runnable baseline이 무엇인가" 혹은 "공식 답 직전에 무엇을 더 단단하게 만드는가"를 실제 코드와 테스트만으로 설명한다.

## 01-mcp-recommendation-demo

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [v0-initial-demo-python](v0-initial-demo-python_answer.md) | 처음 보는 사람도 로컬에서 바로 실행해 볼 수 있는 상담 품질 QA Ops baseline을 만든다. 품질 평가 파이프라인과 운영 UI를 한 번 끝까지 연결해 보는 것이 핵심이다. 핵심은 get_session와 dependency_unavailable_response, lifespan 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v0-initial-demo/python && python3 -m pytest` |
| [v0-initial-demo-react](v0-initial-demo-react_answer.md) | 시작 위치의 구현을 완성해 registry seed와 manifest validation, baseline selector와 한국어 추천 근거, offline eval과 기본 운영 화면을 한 흐름으로 설명하고 검증한다. 핵심은 metadata와 capabilityOptions, apiBaseUrl 흐름을 구현하고 테스트를 통과시키는 것이다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e` |
| [v1-ranking-hardening-react](v1-ranking-hardening-react_answer.md) | 시작 위치의 구현을 완성해 reranker와 compare runner, usage/feedback/experiment API, 운영 콘솔의 compare 화면을 한 흐름으로 설명하고 검증한다. 핵심은 metadata와 apiBaseUrl, apiFetch 흐름을 구현하고 테스트를 통과시키는 것이다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm dev && pnpm test && pnpm eval && pnpm capture:presentation && pnpm e2e` |
| [v1-regression-hardening-python](v1-regression-hardening-python_answer.md) | v0를 바탕으로 회귀 안정성과 lineage를 강화해, 개선 실험이 실제로 나아졌는지 비교 가능한 상태를 만든다. 핵심은 get_session와 dependency_unavailable_response, lifespan 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/python && python3 -m pytest` |
| [v1-regression-hardening-react](v1-regression-hardening-react_answer.md) | v0를 바탕으로 회귀 안정성과 lineage를 강화해, 개선 실험이 실제로 나아졌는지 비교 가능한 상태를 만든다. 핵심은 BASE_URL와 apiGet, apiPost 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.

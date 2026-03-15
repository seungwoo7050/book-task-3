# infobank 종합 과제 답안지

이 문서는 인포뱅크 capstone을 "공식 제출 답"과 "제품형 확장 답"으로 나눠 설명하는 답안지다. 각 항목은 실제 node/python/react source와 테스트만을 근거로, 왜 이 버전이 공식 답인지 혹은 확장 답인지 재구성할 수 있게 적는다.

## 01-mcp-recommendation-demo

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [v2-submission-polish-python](v2-submission-polish-python_answer.md) | v1을 바탕으로 개선 실험 결과를 다시 증빙하고, 최종 runbook과 발표 자료까지 포함한 제출 마감본을 만든다. 핵심은 get_session와 dependency_unavailable_response, lifespan 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python && python3 -m pytest` |
| [v2-submission-polish-react](v2-submission-polish-react_answer.md) | 시작 위치의 구현을 완성해 compatibility gate와 release gate, artifact export와 제출용 proof 문서, 최종 시연 runbook과 compare artifact를 한 흐름으로 설명하고 검증한다. 핵심은 metadata와 apiBaseUrl, apiFetch 흐름을 구현하고 테스트를 통과시키는 것이다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm eval && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation && pnpm test && pnpm e2e` |
| [v3-oss-hardening](v3-oss-hardening_answer.md) | anonymous request가 protected route에서 401을 반환한다. viewer mutation이 403을 반환한다. owner는 user/settings를 관리할 수 있다. operator는 catalog/experiment/release candidate CRUD와 job 실행이 가능하다. 핵심은 sessionCookieOptions와 ensureSettings, buildApp 흐름을 구현하고 테스트를 통과시키는 것이다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation` |
| [v3-self-hosted-oss-python](v3-self-hosted-oss-python_answer.md) | v3-self-hosted-oss의 목표는 v2를 single-team self-hosted QA Ops 도구로 끌어올리는 것이다. 데모가 아니라 설치 가능한 운영형 아카이브로 한 단계 더 확장하는 버전이다. 핵심은 get_session와 get_current_admin, get_current_admin_optional 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.

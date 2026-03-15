# infobank 종합 과제 문제지

`infobank`의 capstone은 stage로 나눠 익힌 계약, 실험, 운영 규칙을 하나의 공식 제출 답과 확장 답으로 다시 묶게 만드는 종합 과제입니다. 여기서는 "공식 제출용 완성본"과 "제품화 확장본"만 남깁니다.

## 01-mcp-recommendation-demo

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [v2-submission-polish-python](v2-submission-polish-python.md) | v1을 바탕으로 개선 실험 결과를 다시 증빙하고, 최종 runbook과 발표 자료까지 포함한 제출 마감본을 만든다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v2-submission-polish/python && python3 -m pytest` |
| [v2-submission-polish-react](v2-submission-polish-react.md) | 시작 위치의 구현을 완성해 compatibility gate와 release gate, artifact export와 제출용 proof 문서, 최종 시연 runbook과 compare artifact를 한 흐름으로 설명하고 검증한다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm eval && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation && pnpm test && pnpm e2e` |
| [v3-oss-hardening](v3-oss-hardening.md) | anonymous request가 protected route에서 401을 반환한다. viewer mutation이 403을 반환한다. owner는 user/settings를 관리할 수 있다. operator는 catalog/experiment/release candidate CRUD와 job 실행이 가능하다. | `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm bootstrap:owner && pnpm build && pnpm test && pnpm test:integration && pnpm e2e && pnpm eval && pnpm compare && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation` |
| [v3-self-hosted-oss-python](v3-self-hosted-oss-python.md) | v3-self-hosted-oss의 목표는 v2를 single-team self-hosted QA Ops 도구로 끌어올리는 것이다. 데모가 아니라 설치 가능한 운영형 아카이브로 한 단계 더 확장하는 버전이다. | `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v3-self-hosted-oss/python && python3 -m pytest` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.

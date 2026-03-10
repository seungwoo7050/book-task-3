# 03-rule-and-guardrail-engine Notion 문서 안내

이 폴더는 **Rule & Guardrail Engine** 단계의 개발 과정과 의사결정을 기록한 블로그형 에세이 모음입니다.

## 어떤 문서를 먼저 읽을까?

| 목적 | 문서 |
|------|------|
| 왜 안전 규칙을 코드로 잡아야 하는지 알고 싶다 | [00-problem-framing.md](./00-problem-framing.md) |
| failure type을 왜 4개로 나눴는지 궁금하다 | [01-approach-log.md](./01-approach-log.md) |
| escalation 규칙 분리 문제를 보고 싶다 | [02-debug-log.md](./02-debug-log.md) |
| 규칙 기반 접근의 한계를 알고 싶다 | [03-retrospective.md](./03-retrospective.md) |
| guardrail과 failure taxonomy 개념을 정리하고 싶다 | [04-knowledge-index.md](./04-knowledge-index.md) |
| 파일 생성 순서와 CLI를 따라가고 싶다 | [05-development-timeline.md](./05-development-timeline.md) |

## 이 문서들과 소스코드의 관계

소스코드(`guardrails.py`, `rules.json`)는 각 규칙의 검출 로직을 보여줍니다.
이 문서들은 **왜 mandatory notice와 escalation을 별도 failure type으로 나눴는지**, **왜 LLM classifier 대신 keyword matching을 선택했는지** 등 설계 의도를 설명합니다.

## 관련 stage

- **이전**: [02-domain-fixtures-and-chat-harness](../../02-domain-fixtures-and-chat-harness/notion/) — 도메인 데이터와 대화 재현
- **다음**: [04-claim-and-evidence-pipeline](../../04-claim-and-evidence-pipeline/notion/) — 주장 추출과 근거 검증 파이프라인

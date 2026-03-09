# 02-domain-fixtures-and-chat-harness Notion 문서 안내

이 폴더는 **Domain Fixtures & Chat Harness** 단계의 개발 과정과 의사결정을 기록한 블로그형 에세이 모음입니다.

## 어떤 문서를 먼저 읽을까?

| 목적 | 문서 |
|------|------|
| 왜 fixture와 harness를 분리했는지 알고 싶다 | [00-problem-framing.md](./00-problem-framing.md) |
| keyword matching을 왜 선택했는지 궁금하다 | [01-approach-log.md](./01-approach-log.md) |
| 짧은 한국어 질의 매칭 문제를 보고 싶다 | [02-debug-log.md](./02-debug-log.md) |
| 이 단계의 한계를 솔직하게 알고 싶다 | [03-retrospective.md](./03-retrospective.md) |
| seeded KB, replay harness 개념을 정리하고 싶다 | [04-knowledge-index.md](./04-knowledge-index.md) |
| 파일 생성 순서와 CLI를 따라가고 싶다 | [05-development-timeline.md](./05-development-timeline.md) |

## 이 문서들과 소스코드의 관계

소스코드는 `harness.py`의 검색 로직과 `data/` 아래 fixture 파일들을 보여줍니다.
이 문서들은 **왜 vector DB 없이 keyword로 시작했는지**, **fixture를 왜 JSON과 Markdown으로 나눴는지**, **한국어 단어 매칭에서 뭐가 안 됐는지** 등 소스코드에 없는 이야기를 담고 있습니다.

## 관련 stage

- **이전**: [01-quality-rubric-and-score-contract](../../01-quality-rubric-and-score-contract/notion/) — 품질 점수 체계
- **다음**: [03-rule-and-guardrail-engine](../../03-rule-and-guardrail-engine/notion/) — 안전 규칙과 가드레일 엔진

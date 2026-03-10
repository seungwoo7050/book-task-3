# 05-judge-and-score-merge Notion 문서 안내

이 폴더는 **Judge & Score Merge** 단계의 개발 과정과 의사결정을 기록한 블로그형 에세이 모음입니다.

## 어떤 문서를 먼저 읽을까?

| 목적 | 문서 |
|------|------|
| judge와 scorer를 왜 분리해야 하는지 알고 싶다 | [00-problem-framing.md](./00-problem-framing.md) |
| heuristic judge를 왜 선택했는지 궁금하다 | [01-approach-log.md](./01-approach-log.md) |
| resolution과 communication 점수 구분 문제를 보고 싶다 | [02-debug-log.md](./02-debug-log.md) |
| heuristic 접근의 한계를 알고 싶다 | [03-retrospective.md](./03-retrospective.md) |
| judge output schema 개념을 정리하고 싶다 | [04-knowledge-index.md](./04-knowledge-index.md) |
| 파일 생성과 CLI 순서를 따라가고 싶다 | [05-development-timeline.md](./05-development-timeline.md) |

## 이 문서들과 소스코드의 관계

소스코드(`judge.py`)는 heuristic 판단과 점수 합산 로직을 보여줍니다.
이 문서들은 **왜 judge가 total까지 계산하면 안 되는지**, **왜 live LLM 대신 heuristic으로 시작했는지** 등 설계의 맥락을 설명합니다.

## 관련 stage

- **이전**: [04-claim-and-evidence-pipeline](../../04-claim-and-evidence-pipeline/notion/) — 주장 추출과 근거 검증
- **다음**: [06-golden-set-and-regression](../../06-golden-set-and-regression/notion/) — 골든 세트 기반 회귀 테스트

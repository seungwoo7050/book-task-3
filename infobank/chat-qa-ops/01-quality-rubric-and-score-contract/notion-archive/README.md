# 01-quality-rubric-and-score-contract Notion 문서 안내

이 폴더는 **Quality Rubric & Score Contract** 단계의 개발 과정과 의사결정을 기록한 블로그형 에세이 모음입니다.

## 어떤 문서를 먼저 읽을까?

| 목적 | 문서 |
|------|------|
| 이 단계가 왜 필요한지 알고 싶다 | [00-problem-framing.md](./00-problem-framing.md) |
| rubric을 왜 이렇게 설계했는지 궁금하다 | [01-approach-log.md](./01-approach-log.md) |
| critical override 관련 버그를 보고 싶다 | [02-debug-log.md](./02-debug-log.md) |
| 끝나고 난 뒤의 평가를 읽고 싶다 | [03-retrospective.md](./03-retrospective.md) |
| weighted rubric 개념을 이해하고 싶다 | [04-knowledge-index.md](./04-knowledge-index.md) |
| 파일 작성과 CLI 순서를 따라가고 싶다 | [05-development-timeline.md](./05-development-timeline.md) |

## 이 문서들과 소스코드의 관계

소스코드(`python/src/stage01/rubric.py`, `python/tests/test_rubric.py`)는 점수 계산 로직을 보여줍니다.
이 문서들은 **왜 weight를 저렇게 나눴는지**, **critical override를 왜 별도 분기로 처리했는지**, **grade band 임계값의 근거가 무엇인지** 등 코드에는 없는 맥락을 제공합니다.

## 관련 stage

- **이전**: [00-source-brief](../../00-source-brief/notion/) — 프로젝트 정의와 참조 자료 구성
- **다음**: [02-domain-fixtures-and-chat-harness](../../02-domain-fixtures-and-chat-harness/notion/) — 테스트용 도메인 데이터와 대화 재현 도구

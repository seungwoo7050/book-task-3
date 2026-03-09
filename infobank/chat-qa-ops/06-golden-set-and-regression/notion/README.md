# Stage 06 — Golden Set & Regression 노트 가이드

이 폴더는 chat-qa-ops의 여섯 번째 stage인 **Golden Set & Regression**의 설계 과정과 의사결정 기록을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 회귀 탐지가 왜 필요한지, golden set이라는 접근이 어떻게 나왔는지 |
| 2 | [01-approach-log.md](./01-approach-log.md) | golden case 설계, evaluate_case 구현, compare manifest 구조 결정 과정 |
| 3 | [02-debug-log.md](./02-debug-log.md) | reason code 설계 시 겪은 문제와 해결 |
| 4 | [03-retrospective.md](./03-retrospective.md) | golden set 기반 회귀 방식의 장단점 정리 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | golden case, reason code, compare manifest 등 핵심 개념 사전 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | CLI 명령어, 파일 생성 순서, 테스트 실행 흐름 |

## 관련 stage

- **이전**: [05-judge-and-score-merge](../../05-judge-and-score-merge/notion/) — judge가 생산한 점수를 여기서 baseline 대비 비교한다
- **다음**: [07-monitoring-dashboard](../../07-monitoring-dashboard-and-review-console/notion/) — 회귀 결과를 대시보드에서 시각화한다

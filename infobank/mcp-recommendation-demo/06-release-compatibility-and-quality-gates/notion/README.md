# Stage 06 — Release Compatibility & Quality Gates 노트 가이드

이 폴더는 mcp-recommendation-demo의 일곱 번째 stage인 **Release Compatibility & Quality Gates**의 설계 과정을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 도구 업데이트 시 호환성과 품질을 왜 자동 검증해야 하는지 |
| 2 | [01-approach-log.md](./01-approach-log.md) | compatibility gate, release gate, artifact export 설계 |
| 3 | [02-debug-log.md](./02-debug-log.md) | semver 파싱, gate 판정 로직, artifact 형식 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | gate 기반 릴리즈 관리의 효과와 한계 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | release candidate, compatibility, gate, artifact 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | service 구현, CLI 명령어, test 작성 순서 |

## 관련 stage

- **이전**: [05-usage-logs](../../05-usage-logs-metrics-and-feedback-loop/notion/) — usage 데이터가 release gate 판정 참고
- **다음**: [07-operator-dashboard](../../07-operator-dashboard-and-experiment-console/notion/) — gate 결과를 대시보드에서 시각화

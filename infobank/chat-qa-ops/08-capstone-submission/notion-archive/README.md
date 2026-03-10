# Stage 08 — Capstone Submission 노트 가이드

이 폴더는 chat-qa-ops의 마지막 stage인 **Capstone Submission**의 설계 과정과 의사결정 기록을 담고 있다.
Capstone은 v0부터 v3까지 4개 버전으로 점진적으로 발전한다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 왜 4단계 버전이 필요한지, 각 버전의 목적 |
| 2 | [01-approach-log.md](./01-approach-log.md) | v0→v1→v2→v3 전환 시 핵심 의사결정 |
| 3 | [02-debug-log.md](./02-debug-log.md) | provider chain, PostgreSQL 전환, Docker Compose 문제 해결 |
| 4 | [03-retrospective.md](./03-retrospective.md) | 4-version 점진 개선 방식의 장단점 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | 버전별 기술 스택, 품질 지표, 아키텍처 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | v0부터 v3까지 CLI 명령어, 패키지 설치, 배포 흐름 |

## 관련 stage

- **이전**: stage 00~07의 모든 모듈이 여기서 통합된다
- stage 00(source_brief) → v0 기준 정의
- stage 01(rubric) → 모든 버전에서 사용
- stage 02(harness) → v0 replay, v2 retrieval-v2
- stage 03(guardrails) → v0~ failure_types
- stage 04(pipeline) → v0~ claim verification
- stage 05(judge) → v0 heuristic, v1 LLM judge
- stage 06(golden set) → v0~ regression, v2 compare artifact
- stage 07(dashboard) → v0~ React UI

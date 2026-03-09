# Stage 07 — Monitoring Dashboard & Review Console 노트 가이드

이 폴더는 chat-qa-ops의 일곱 번째 stage인 **Monitoring Dashboard & Review Console**의 설계 과정과 의사결정 기록을 담고 있다.

## 문서 읽는 순서

| 순서 | 파일 | 내용 |
|------|------|------|
| 1 | [00-problem-framing.md](./00-problem-framing.md) | 운영 대시보드가 왜 필요한지, snapshot 방식의 API를 선택한 이유 |
| 2 | [01-approach-log.md](./01-approach-log.md) | FastAPI snapshot API와 React 대시보드 4페이지 설계 과정 |
| 3 | [02-debug-log.md](./02-debug-log.md) | version compare UI, i18n 처리 등에서 겪은 문제 |
| 4 | [03-retrospective.md](./03-retrospective.md) | snapshot 방식의 장단점, 실시간 전환 시 고려사항 |
| 5 | [04-knowledge-index.md](./04-knowledge-index.md) | API 엔드포인트, React 페이지 구조, lineage 개념 정리 |
| 6 | [05-development-timeline.md](./05-development-timeline.md) | CLI 명령어, 패키지 설치, 프로젝트 구조 생성 순서 |

## 관련 stage

- **이전**: [06-golden-set-and-regression](../../06-golden-set-and-regression/notion/) — golden run 결과와 version compare 데이터를 이 대시보드에서 표시한다
- **다음**: [08-capstone-submission](../../08-capstone-submission/notion/) — 대시보드를 포함한 전체 시스템을 통합한다

# D-data-jpa-lab — Notion 문서 가이드

이 폴더는 D-data-jpa-lab의 개발 과정과 설계 결정을 기록한 문서 모음이다. JPA를 단순한 CRUD 도구가 아니라 설계 선택이 드러나는 도구로 다루는 과정을 담고 있다.

## 문서 구성

| 순번 | 문서 | 핵심 질문 |
|------|------|-----------|
| 00 | [Problem Framing](00-problem-framing.md) | 이 랩은 왜 존재하고 무엇을 다루는가? |
| 01 | [Approach Log](01-approach-log.md) | 세 가지 선택지 중 왜 이 방향을 택했는가? |
| 02 | [Debug Log](02-debug-log.md) | Keyword inflation이란 무엇이고 어떻게 대응했는가? |
| 03 | [Retrospective](03-retrospective.md) | 무엇이 나아지고 무엇이 아직 약한가? |
| 04 | [Knowledge Index](04-knowledge-index.md) | 재사용 가능한 개념과 용어는 무엇인가? |
| 05 | [Timeline](05-timeline.md) | 소스 코드에서 보이지 않는 개발 과정은? |

## 목적별 읽기 가이드

### "이 프로젝트가 뭔지 빠르게 알고 싶다"
→ [00-problem-framing.md](00-problem-framing.md)의 "이 랩이 존재하는 이유"와 "구체적으로 무엇을 다루는가" 섹션을 읽는다.

### "JPA에서 entity와 service를 왜 나누는지 궁금하다"
→ [01-approach-log.md](01-approach-log.md)의 "패키지 구조: 계층이 보이는 코드" 섹션에서 설계 근거를 확인하고, [04-knowledge-index.md](04-knowledge-index.md)의 "Entity와 Service의 경계 분리" 개념을 읽는다.

### "낙관적 락이 어떻게 동작하는지 알고 싶다"
→ [04-knowledge-index.md](04-knowledge-index.md)의 "낙관적 락" 섹션에서 `@Version` 자동 동작과 애플리케이션 레벨 수동 확인의 차이를 설명한다. [05-timeline.md](05-timeline.md)의 Phase 6에서 테스트 시나리오의 4단계 흐름을 확인한다.

### "Querydsl이 설치되어 있는데 왜 안 쓰는 건지 궁금하다"
→ [02-debug-log.md](02-debug-log.md)에서 "keyword inflation" 문제를 다루고 있다. [00-problem-framing.md](00-problem-framing.md)의 "의도적으로 다루지 않는 것들"에서 현재 단계의 범위 제한 이유를 설명한다.

### "Flyway와 JPA를 왜 같이 쓰는지 알고 싶다"
→ [04-knowledge-index.md](04-knowledge-index.md)의 "Flyway + JPA validate 조합" 섹션과 [05-timeline.md](05-timeline.md)의 Phase 2에서 마이그레이션 SQL 작성 과정을 확인한다.

### "이 프로젝트를 처음부터 따라 만들고 싶다"
→ [05-timeline.md](05-timeline.md)를 Phase 1부터 순서대로 따라간다. CLI 명령어, 설정 파일 변경, 설계 결정의 이유가 시간 순서대로 정리되어 있다.

### "면접에서 이 프로젝트를 설명하고 싶다"
→ [03-retrospective.md](03-retrospective.md)에서 "나아진 점"과 "아직 약한 점"을 중심으로 설명한다. "entity 경계가 보이기 시작했다"는 것과 "Querydsl 깊이가 부족하다"는 것을 솔직하게 말할 수 있어야 한다.

## 관련 문서

- [docs/README.md](../docs/README.md) — 현재 구현 범위와 단순화, 다음 개선 방향
- [problem/README.md](../problem/README.md) — 한 줄 문제 정의
- [spring/README.md](../spring/README.md) — 빌드, 실행, 테스트 명령어

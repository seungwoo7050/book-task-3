# D-data-jpa-lab 학습 노트 가이드

이 폴더는 JPA를 설계 선택으로 읽는 과정을 기록한 공개 학습 노트 세트다.

## 먼저 읽을 문서

1. [00-problem-framing.md](00-problem-framing.md): 왜 이 랩이 존재하는지와 현재 범위
2. [05-development-timeline.md](05-development-timeline.md): Flyway, entity, 테스트를 어떤 순서로 쌓았는지
3. [01-approach-log.md](01-approach-log.md): 계층 구조와 persistence 선택을 왜 이렇게 잡았는지

## 목적별 읽기

- keyword inflation을 어떻게 피했는지 보려면 [02-debug-log.md](02-debug-log.md)
- optimistic locking, Flyway + JPA validate 조합을 복습하려면 [04-knowledge-index.md](04-knowledge-index.md)
- 현재 강점과 한계를 정리하려면 [03-retrospective.md](03-retrospective.md)

## 문서 목록

- `00-problem-framing.md`: 문제 정의와 성공 기준
- `01-approach-log.md`: 설계 선택지와 최종 결정
- `02-debug-log.md`: 실패와 수정 근거
- `03-retrospective.md`: 강점, 약점, 다음 단계
- `04-knowledge-index.md`: 개념과 참고 자료
- `05-development-timeline.md`: 재현 가능한 개발 순서 기록

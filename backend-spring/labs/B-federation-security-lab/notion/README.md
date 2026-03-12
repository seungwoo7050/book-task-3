# B-federation-security-lab 학습 노트 가이드

이 폴더는 federation, 2FA, audit를 한 랩으로 묶은 이유와 그 과정에서의 판단을 기록한 공개 학습 노트 세트다.

## 먼저 읽을 문서

1. [00-problem-framing.md](00-problem-framing.md): 왜 federation, 2FA, audit를 함께 다루는가
2. [05-development-timeline.md](05-development-timeline.md): 로컬에서 다시 재현할 때 따라갈 순서
3. [01-approach-log.md](01-approach-log.md): real integration 대신 contract modeling을 먼저 택한 이유

## 목적별 읽기

- 보안 기능 과장과 문서화 함정을 보려면 [02-debug-log.md](02-debug-log.md)
- external identity linking, TOTP, audit 개념을 복습하려면 [04-knowledge-index.md](04-knowledge-index.md)
- 현재 한계와 다음 확장을 보려면 [03-retrospective.md](03-retrospective.md)

## 문서 목록

- `00-problem-framing.md`: 문제 정의와 성공 기준
- `01-approach-log.md`: 선택지 비교와 최종 방향
- `02-debug-log.md`: 실패와 과장 방지 기록
- `03-retrospective.md`: 강점, 약점, 다음 단계
- `04-knowledge-index.md`: 핵심 개념과 용어
- `05-development-timeline.md`: 재현 가능한 개발 순서 기록

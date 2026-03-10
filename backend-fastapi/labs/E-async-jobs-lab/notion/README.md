# E-async-jobs-lab 학습 노트

이 폴더는 현재 공개용 학습 노트입니다. 비동기 handoff와 worker 흐름을 이 노트 세트만으로 따라갈 수 있게 정리했습니다.

## 먼저 볼 문서

- 바로 손을 움직여 재현하고 싶다면 [05-development-timeline.md](05-development-timeline.md)부터 읽습니다.
- 왜 이런 구조로 만들었는지부터 이해하고 싶다면 `00`, `01`부터 읽습니다.

## 추천 읽기 순서

1. [00-problem-framing.md](00-problem-framing.md)
2. [01-approach-log.md](01-approach-log.md)
3. [02-debug-log.md](02-debug-log.md)
4. [03-retrospective.md](03-retrospective.md)
5. [04-knowledge-index.md](04-knowledge-index.md)
6. [05-development-timeline.md](05-development-timeline.md)

## 어떻게 쓰면 좋은가

- 실행 재현이 최우선이면 `05`를 먼저 보고, enqueue와 outbox 경계의 의도는 `01`에서 다시 읽습니다.
- outbox와 idempotency 개념을 먼저 잡으려면 `00`, `01`을 읽습니다.
- eager mode나 retry 상태 문제를 보고 싶다면 `02`가 가장 빠릅니다.
- 자기 포트폴리오의 비동기 경계를 설계할 때는 `03`, `04`를 참고하면 됩니다.

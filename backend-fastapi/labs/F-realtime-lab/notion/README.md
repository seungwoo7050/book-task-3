# F-realtime-lab 학습 노트

이 폴더는 현재 공개용 학습 노트입니다. WebSocket, presence, fan-out의 핵심을 이 노트만으로 복기할 수 있게 정리했습니다.

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

- 실행 재현이 최우선이면 `05`를 먼저 보고, 연결 수명주기 설계는 `01`, `02`에서 다시 읽습니다.
- WebSocket, presence, fan-out의 경계를 먼저 이해하려면 `00`, `01`을 읽습니다.
- 시간 경계나 connection cleanup 같은 함정은 `02`에서 빠르게 확인할 수 있습니다.
- 확장형 실시간 구조를 고민할 때는 `03`, `04`가 도움 됩니다.

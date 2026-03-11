# arenaserv 지식 색인

## 핵심 개념

- session continuity: 접속이 잠시 끊겨도 상태를 이어 가게 하는 설계
- room state machine: queue, ready, in-round, finished를 잇는 전이 규칙
- authoritative event: 서버만이 확정할 수 있는 snapshot, hit, elimination, round end

## 먼저 볼 파일

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_arenaserv.py](../cpp/tests/test_arenaserv.py)

## 비교하면 좋은 프로젝트

- `ticklab`: simulation만 먼저 검증한 버전
- `ircserv`: 같은 저장소의 다른 capstone이 범위를 끊는 방식

## 백업 자료

- 예전 버전 노트와 타임라인은 [../notion-archive/](../notion-archive/)에 있다.

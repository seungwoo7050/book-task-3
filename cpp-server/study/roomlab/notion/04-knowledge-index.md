# roomlab 지식 색인

## 핵심 개념

- registration state: 사용자가 아직 완전한 IRC 세션이 되지 않은 구간
- room lifecycle: 생성, join, leave, cleanup까지의 전체 흐름
- cleanup: 종료 후 남은 인덱스와 버퍼를 정리하는 단계

## 먼저 볼 파일

- [../cpp/src/Connection.cpp](../cpp/src/Connection.cpp)
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp)
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)

## 다음 프로젝트와의 연결

- `ircserv`: 고급 channel command와 capstone 범위
- `arenaserv`: 다른 도메인에서도 상태 전이와 cleanup이 얼마나 중요한지 비교

## 백업 자료

- 예전 버전 노트와 타임라인은 [../notion-archive/](../notion-archive/)에 있다.

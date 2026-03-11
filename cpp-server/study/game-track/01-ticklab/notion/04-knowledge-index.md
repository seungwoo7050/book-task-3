# ticklab 지식 색인

## 핵심 개념

- fixed-step simulation: 고정된 tick마다 상태를 전진시키는 방식
- stale input rejection: 이미 지난 상태를 다시 덮지 않도록 입력을 거절하는 규칙
- snapshot regeneration: reconnect 뒤 상태를 다시 이어 붙이기 위한 복구 데이터

## 먼저 볼 파일

- [../cpp/include/inc/MatchEngine.hpp](../cpp/include/inc/MatchEngine.hpp)
- [../cpp/src/MatchEngine.cpp](../cpp/src/MatchEngine.cpp)
- [../cpp/tests/test_ticklab.cpp](../cpp/tests/test_ticklab.cpp)

## 다음 프로젝트와의 연결

- `arenaserv`: simulation을 실제 TCP 서버에 붙이는 단계
- `eventlab`: 런타임 기반이 simulation 바깥에서 어떻게 작동하는지 비교

## 백업 자료

- 예전 버전 노트와 타임라인은 [../notion-archive/](../notion-archive/)에 있다.

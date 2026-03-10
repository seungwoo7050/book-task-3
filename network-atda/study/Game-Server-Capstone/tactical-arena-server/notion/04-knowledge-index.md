# 04 지식 인덱스

## 핵심 용어
- **authoritative server**: 게임 상태의 최종 진실을 서버가 결정하는 구조다.
- **`strand`**: Boost.Asio에서 특정 작업 흐름을 직렬화해 동시 접근을 방지하는 도구다.
- **snapshot**: 서버가 일정 주기로 클라이언트에 뿌리는 현재 월드 상태 요약이다.
- **resume token**: 끊긴 TCP 세션을 같은 플레이어 상태로 복구하기 위한 식별자다.

## 다시 볼 파일
- [`../problem/code/control-protocol.txt`](../problem/code/control-protocol.txt): TCP 제어 프로토콜의 문법과 명령 집합 기준 문서다.
- [`../cpp/src/arena_server.cpp`](../cpp/src/arena_server.cpp): 세션 관리, room/match 상태 전이, TCP/UDP 통합 흐름이 모두 들어 있다.
- [`../cpp/src/state.cpp`](../cpp/src/state.cpp): authoritative 시뮬레이션과 경기 종료 조건을 읽을 때 핵심이 된다.
- [`../problem/script/integration_test.py`](../problem/script/integration_test.py): reconnect, forfeit, out-of-order UDP 같은 고난도 시나리오를 어떻게 재현하는지 보여준다.
- [`../docs/concepts/architecture.md`](../docs/concepts/architecture.md): 전체 계층 구조를 빠르게 다시 잡을 때 가장 먼저 읽는다.

## 자주 쓰는 확인 명령
- `make -C study/Game-Server-Capstone/tactical-arena-server/problem test`
- `cmake -S study/Game-Server-Capstone/tactical-arena-server/cpp -B study/Game-Server-Capstone/tactical-arena-server/cpp/build && cmake --build study/Game-Server-Capstone/tactical-arena-server/cpp/build`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음

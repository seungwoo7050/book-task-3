# eventlab 지식 색인

## 핵심 개념

- non-blocking socket: 한 클라이언트가 느려도 전체 서버가 멈추지 않게 하는 기본 전제
- readiness event: 지금 읽거나 쓸 준비가 됐다는 커널 신호
- keep-alive: 연결이 살아 있는지 확인하는 애플리케이션 계층 계약

## 먼저 볼 파일

- [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp)
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)

## 다음 프로젝트와의 연결

- `msglab`: 입력을 구조화하는 법
- `roomlab`: 연결 위에 상태 전이를 올리는 법
- `arenaserv`: 같은 런타임 기반을 게임 서버에 적용하는 법

## 백업 자료

- 예전 초안과 긴 타임라인은 [../notion-archive/](../notion-archive/)에 있다.

# eventlab 문제 재구성

이 문서는 현재 저장소의 구현, 테스트, 보존된 기록을 바탕으로 다시 정리한 학습용 문제 설명이다. 원본 과제지는 남아 있지 않으므로, 지금 이 레포 안에서 직접 확인 가능한 범위만 문제로 선언한다.

## 학습 목표

- non-blocking TCP 서버의 최소 event loop를 직접 관찰한다.
- 연결 수명주기를 IRC나 게임 규칙과 분리해 이해한다.
- 작은 텍스트 프로토콜 위에서 smoke test를 작성해 런타임 동작을 검증한다.

## 구현해야 할 것

- 지정한 포트에 listening socket을 열기
- 여러 클라이언트를 동시에 accept하고 read/write 이벤트 처리하기
- 줄 단위 텍스트 프로토콜 지원하기
- `PING <token>`에 `PONG <token>` 응답하기
- 일반 입력을 `ECHO <line>`으로 되돌리기
- idle connection에 keep-alive를 보내고 응답이 없으면 정리하기

## 산출물

- event loop abstraction을 사용하는 C++17 서버
- 다중 연결 smoke test

## 범위에서 제외하는 것

- IRC command parsing
- channel state와 registration
- authoritative simulation이나 게임 규칙

## 현재 저장소에서 확인할 수 있는 근거

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp): accept, read, write, keep-alive 흐름
- [../cpp/src/EventManager.cpp](../cpp/src/EventManager.cpp): 이벤트 루프 추상화
- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py): 현재 검증 시나리오
- [../notion-archive/00-problem-framing.md](../notion-archive/00-problem-framing.md): 이전 문제 정의 메모 백업

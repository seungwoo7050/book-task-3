# roomlab 디버그 노트

이 문서는 현재 구현 기준으로, room lifecycle과 registration에서 특히 흔들리기 쉬운 실패 지점을 다시 정리한 백업 노트다. 긴 기록은 [../notion-archive/](../notion-archive/)에 남겨 두었다.

## 사례 1. duplicate nick 검사가 registration 흐름과 어긋나는 문제

### 증상

[../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)에서 세 번째 클라이언트가 이미 사용 중인 `alice`로 등록을 시도할 때 `433`이 정확한 시점에 오지 않거나, 이후 상태가 이상하게 섞인다.

### 왜 중요하나

duplicate nick은 작은 에러처럼 보이지만 registration state machine의 경계를 점검하는 가장 좋은 지표다. 검사 타이밍이 늦으면 "이미 등록된 것처럼 보였다가 다시 실패하는" 어색한 상태가 생길 수 있다.

### 지금 확인할 파일

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)

## 사례 2. room membership을 한쪽 인덱스만 정리하는 문제

### 증상

JOIN과 PART는 되는 것처럼 보이는데, 이후 cleanup이나 후속 명령에서 stale state가 남는다.

### 왜 위험한가

room membership은 서버 전역 구조와 connection 로컬 구조가 함께 움직여야 한다. 한쪽만 바꾸면 지금은 통과해도 나중에 broadcast, PART, cleanup 순서에서 버그가 되돌아온다.

### 지금 확인할 파일

- [../cpp/src/Connection.cpp](../cpp/src/Connection.cpp)
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp)

코드를 읽을 때는 "누가 채널에 속하는지"가 한 군데가 아니라 양쪽에 어떻게 반영되는지 보는 것이 좋다.

## 사례 3. `QUIT`과 disconnect cleanup을 같은 것으로 보는 문제

### 증상

종료 경로를 단순화하려고 `QUIT`과 네트워크 disconnect를 같은 cleanup으로 묶고 싶어진다.

### 왜 위험한가

`QUIT`은 다른 멤버에게 broadcast할 메시지가 있는 종료다. 반면 disconnect는 말 없이 끊어진 연결일 수 있다. 둘을 같은 경로로 설명하면 broadcast 시점과 자원 정리 순서가 흐려진다.

### 지금 확인할 파일

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)

테스트에서는 alice의 `QUIT :gone away`가 bob에게 전달되는지 확인한다. 이 시나리오는 cleanup 이전에 broadcast가 먼저 있어야 한다는 점을 보여 준다.

## 다시 막히면 따를 순서

1. registration 상태가 올바르게 전이되는지 본다.
2. room membership이 서버와 connection 양쪽에 반영되는지 본다.
3. cleanup 이전과 이후에 어떤 메시지가 나가야 하는지 구분한다.

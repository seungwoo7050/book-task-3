# eventlab 디버그 노트

이 문서는 현재 구현을 기준으로, 실제로 부딪히기 쉬운 실패 지점을 "증상, 원인, 수정 방향, 확인 방법" 순서로 다시 정리한 백업 노트다. 더 긴 시간순 기록은 [../notion-archive/](../notion-archive/)에 남겨 두었다.

## 사례 1. keep-alive가 제시간에 안 보이는 문제

### 증상

[../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)에서 idle keep-alive를 기다리는데 바로 도착하지 않는 것처럼 보인다.

### 왜 생기는가

현재 구조에서 keep-alive 검사는 event loop cycle 시작 시점에만 돈다. 즉, 서버가 새 이벤트를 처리하기 위해 깨어나야 idle 시간을 다시 평가할 수 있다. "시간이 지났으니 자동으로 바로 PING이 간다"라고 기대하면 구조를 오해하게 된다.

### 어떻게 다뤘는가

서버를 더 복잡하게 바꾸기보다, 테스트 쪽에서 이벤트 루프가 다시 한 번 돌도록 작은 자극을 준다. 이 선택은 "현재 구조의 의미"를 드러내는 데 더 적합했다.

### 지금 확인할 파일

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)
- [../cpp/tests/test_eventlab.py](../cpp/tests/test_eventlab.py)

## 사례 2. `QUIT`과 EOF cleanup을 같은 감각으로 처리하는 문제

### 증상

종료 경로가 단순해 보여 `QUIT`과 소켓 EOF를 같은 코드 경로로 묶고 싶어진다.

### 왜 위험한가

`QUIT`은 사용자가 의도를 가지고 종료 메시지를 보낸 경우다. 반면 EOF는 네트워크 단절이나 프로세스 종료처럼 "말 없이 사라진" 경우일 수 있다. 둘을 같은 감각으로 다루면 종료 응답, broadcast, cleanup 순서를 헷갈리기 쉽다.

### 지금 구현에서 보는 포인트

- `QUIT`은 응답을 보내고 종료 흐름으로 들어간다.
- EOF는 읽기 경로에서 더 직접적으로 정리된다.

이 차이를 문서로 남겨 두지 않으면, 다음 프로젝트에서 종료 처리 설명이 쉽게 흐려진다.

## 사례 3. non-blocking write를 한 번의 send로 끝난다고 보는 문제

### 증상

작은 메시지만 다루다 보면 응답이 항상 한 번에 flush될 것처럼 느껴진다.

### 왜 위험한가

non-blocking 환경에서는 write readiness와 send buffer 관리가 read path만큼 중요하다. 읽기 경로만 점검하고 쓰기 큐를 대충 다루면, 지금은 운 좋게 통과해도 다음 lab에서 버그로 되돌아온다.

### 지금 확인할 파일

- [../cpp/src/Server.cpp](../cpp/src/Server.cpp)

write queue에 응답이 쌓이고, 실제 flush가 readiness 시점에 일어나는지 구분해서 읽는 것이 좋다.

## 다시 문제를 만났을 때의 점검 순서

1. 서버가 accept까지 가는지 본다.
2. read readiness 이후 버퍼 처리가 맞는지 본다.
3. 응답이 queue에 쌓이는지, 실제 flush가 되는지 본다.
4. 종료 경로에서 fd 정리가 빠지지 않는지 본다.

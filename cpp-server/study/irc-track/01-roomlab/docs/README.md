# roomlab 개념 메모

이 디렉터리는 IRC subset 서버의 범위를 어디까지 자를지, 그리고 왜 capstone과 나눠 읽어야 하는지 설명한다.

## 먼저 볼 질문

- registration 전후로 허용 명령을 어떻게 나눌 것인가
- room membership과 broadcast는 어떤 인덱스 갱신을 요구하는가
- disconnect cleanup은 왜 기능보다 상태 전이 문제에 가까운가

## 읽기 포인트

- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)
- [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp)
- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)

## 다음 단계

- capstone 비교는 [../../02-ircserv/README.md](../../02-ircserv/README.md)

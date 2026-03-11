# roomlab 문제 프레이밍

## 왜 이 lab이 중요한가

`roomlab`은 “작동하는 작은 서버”라는 감각을 처음 주는 프로젝트다. 여기서부터는 문자열 처리만이 아니라, 등록과 room membership이라는 상태 전이를 실제 연결과 함께 다뤄야 한다.

## 지금 풀어야 하는 질문

- registration 완료 전과 후에 허용 명령을 어떻게 나눌 것인가
- room membership은 어떤 자료구조와 cleanup 규칙을 가져야 하는가
- `QUIT`과 네트워크 disconnect는 어떤 점이 비슷하고 어떤 점이 다른가

## 성공 기준

- [../cpp/tests/test_roomlab.py](../cpp/tests/test_roomlab.py)가 registration, duplicate nick, room broadcast, cleanup을 검증한다.
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)와 [../cpp/src/execute_join.cpp](../cpp/src/execute_join.cpp)를 읽으면 상태 전이 경계가 보인다.
- 이후 `ircserv`로 갈 때 어떤 고급 명령이 추가되는지 분명히 말할 수 있다.

## 포트폴리오 관점에서 중요하게 볼 것

- registration 상태 머신
- room lifecycle과 cleanup
- error path를 포함한 smoke test 증거

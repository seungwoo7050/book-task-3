# roomlab

`roomlab`은 IRC subset 서버의 첫 완성형이다. `eventlab`에서 배운 런타임과 `msglab`에서 정리한 parser 책임을 합쳐, 등록과 room lifecycle이 실제 연결 위에서 어떻게 움직이는지 보여 준다.

## 이 프로젝트가 가르치는 것

- registration 전후로 command surface가 어떻게 달라지는지
- room membership과 broadcast가 어떤 상태 전이를 요구하는지
- duplicate nick, `QUIT`, disconnect cleanup 같은 실전형 예외 처리

## 현재 범위

- 포함: `PASS`, `NICK`, `USER`, `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `PING`, `PONG`, `QUIT`
- 제외: `TOPIC`, `MODE`, `KICK`, `INVITE`, `CAP`, TLS, 서비스 계층

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [cpp/README.md](cpp/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 포트폴리오로 확장할 때 보여 줄 것

- 등록 상태 머신과 room lifecycle을 한 그림으로 설명하기
- duplicate nick, broadcast, cleanup를 재현하는 [cpp/tests/test_roomlab.py](cpp/tests/test_roomlab.py) 같은 증거 남기기
- `ircserv`로 올라가며 어떤 기능이 capstone용으로 추가되는지 비교 표 만들기

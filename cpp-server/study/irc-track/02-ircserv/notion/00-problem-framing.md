# ircserv 문제 프레이밍

## 왜 이 프로젝트가 capstone인가

`ircserv`의 핵심은 기능을 많이 붙이는 데 있지 않다. 앞선 `eventlab`, `msglab`, `roomlab`에서 나눠 본 책임을 다시 한 서버로 합쳐도 여전히 읽기 쉽고 검증 가능하게 유지하는 것이 capstone의 본질이다.

## 지금 풀어야 하는 질문

- roomlab과 비교해 어떤 기능이 정말 capstone 수준의 추가인지
- channel privilege와 advanced command는 어디서부터 복잡해지는지
- raw TCP smoke test로 어느 정도까지 completeness를 보여 줄 수 있는지

## 성공 기준

- [../cpp/tests/test_irc_join.py](../cpp/tests/test_irc_join.py)가 `CAP`, `MODE`, `INVITE`, `TOPIC`, `KICK`, `PING/PONG`를 검증한다.
- [../cpp/src/Executor.cpp](../cpp/src/Executor.cpp)와 [../cpp/src/Channel.cpp](../cpp/src/Channel.cpp)를 읽으면 고급 command의 핵심 책임이 드러난다.
- `roomlab` 대비 무엇이 추가됐는지 표로 설명할 수 있다.

## 포트폴리오 관점에서 중요하게 볼 것

- capstone 범위를 어디서 끊었는가
- client compatibility를 위해 무엇을 최소로 넣었는가
- smoke test가 어느 command surface를 보장하는가

# ircserv Problem

이 문서는 원본 과제 문서가 없는 상태에서 `legacy/` 코드를 바탕으로 재구성한 문제 설명이다.

## Reconstructed Prompt

C++17 pure TCP IRC 서버 `ircserv`를 작성한다. 실행 표면은 다음과 같다.

```sh
./ircserv <port> <password>
```

서버는 `roomlab` 범위의 명령 위에 다음을 추가해야 한다.

- `CAP LS 302`
- `TOPIC`
- `MODE`
- `KICK`
- `INVITE`
- registration 중 `005 ISUPPORT` 광고

## Deliverables

- C++17 capstone IRC server
- raw TCP end-to-end smoke test

## Provenance

| source | why it matters |
| --- | --- |
| `legacy/README.md` | 최종 pure TCP 서버를 어디서 분리해야 하는지 보여주는 상위 맥락 |
| `legacy/src/Server.cpp` | 이벤트 루프, keep-alive, socket lifecycle의 출처 |
| `legacy/src/Executor.cpp` | advanced IRC commands의 출처 |
| `legacy/src/execute_join.cpp` | JOIN/PART와 NAMES reply의 출처 |
| `legacy/src/Channel.cpp` | mode/operator/invite state의 출처 |

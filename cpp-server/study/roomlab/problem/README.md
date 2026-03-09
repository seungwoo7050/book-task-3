# roomlab Problem

이 문서는 원본 과제 문서가 없는 상태에서 `legacy/` 코드를 바탕으로 재구성한 문제 설명이다.

## Reconstructed Prompt

C++17 pure TCP IRC subset 서버를 작성한다. 다음 명령 집합만 지원한다.

- 등록: `PASS`, `NICK`, `USER`
- 채널: `JOIN`, `PART`
- 메시지: `PRIVMSG`, `NOTICE`
- 연결 관리: `PING`, `PONG`, `QUIT`

서버는 중복 닉네임을 거절해야 하고, room 가입/탈퇴와 room broadcast를 처리해야 하며, idle client에 keep-alive를 수행해야 한다.

## Deliverables

- raw TCP mini IRC room server
- 등록/중복 nick/room broadcast/QUIT cleanup smoke test

## Provenance

| source | why it matters |
| --- | --- |
| `legacy/src/Connection.cpp` | connection lifetime 모델의 출처 |
| `legacy/src/Channel.cpp` | channel membership/state의 출처 |
| `legacy/src/Executor.cpp` | PASS/NICK/USER/PRIVMSG/NOTICE/QUIT 처리의 출처 |
| `legacy/src/execute_join.cpp` | JOIN/PART 흐름의 출처 |
| `legacy/src/Server.cpp` | event loop와 disconnect cleanup의 출처 |

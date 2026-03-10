# ircserv

`ircserv`는 IRC 축의 capstone이다. 앞선 `eventlab`, `msglab`, `roomlab`에서 나눠 본 런타임, parser, 상태 전이를 다시 합쳐, pure TCP modern IRC 서버를 한 프로젝트로 보여 준다.

## 이 프로젝트가 가르치는 것

- capstone에서 “기능 추가”보다 “앞선 경계를 다시 합치는 일”이 왜 중요한지
- channel privilege와 state-machine completeness를 어떻게 다뤄야 하는지
- 클라이언트 호환성을 위해 최소한의 `CAP`/`ISUPPORT`가 왜 필요한지

## 현재 범위

- 포함: `CAP`, `PASS`, `NICK`, `USER`, `JOIN`, `PART`, `PRIVMSG`, `NOTICE`, `TOPIC`, `MODE`, `KICK`, `INVITE`, `PING`, `PONG`, `QUIT`
- 제외: TLS, SASL, operator services, full IRCv3 capability set

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [cpp/README.md](cpp/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 포트폴리오로 확장할 때 보여 줄 것

- roomlab 대비 무엇이 capstone 수준으로 추가됐는지 표로 설명하기
- [cpp/tests/test_irc_join.py](cpp/tests/test_irc_join.py) 기반으로 protocol smoke test 증거를 남기기
- 클라이언트 호환성 관점에서 `CAP`/`005 ISUPPORT`를 넣은 이유를 문서화하기

# irc-track blog

이 트랙의 blog 시리즈는 IRC subset 서버를 "작동한다"가 아니라 "어떤 상태 전이를 먼저 고정하고 무엇을 capstone에 남겼는가"라는 관점으로 복원한다. chronology는 공통으로 `problem/README.md`, `cpp/Makefile`, `cpp/src`, `cpp/tests`, `docs/README.md`를 읽고, `roomlab -> ircserv` 순서가 그대로 확장 관계를 드러내게 썼다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| --- | --- | --- |
| roomlab | [README.md](01-roomlab/README.md) | [../../irc-track/01-roomlab/README.md](../../irc-track/01-roomlab/README.md) |
| ircserv | [README.md](02-ircserv/README.md) | [../../irc-track/02-ircserv/README.md](../../irc-track/02-ircserv/README.md) |

## 읽는 순서

1. [roomlab](01-roomlab/README.md)로 registration, `JOIN`/`PART`, broadcast, cleanup 같은 core subset을 먼저 본다.
2. [ircserv](02-ircserv/README.md)로 `CAP`, `MODE`, `TOPIC`, `INVITE`, `KICK`가 기존 상태 전이에 어떻게 올라붙는지 본다.
3. 공용 기반을 다시 보려면 [../shared-core/README.md](../shared-core/README.md), 다른 capstone과 비교하려면 [../game-track/README.md](../game-track/README.md)로 이동한다.

## source-first 메모

- 두 프로젝트 모두 `Server`, `Executor`, `Channel`이 같은 이름을 쓰지만, chronology는 "무엇이 이미 `roomlab`에 있고 무엇이 `ircserv`에서 새로 들어왔는가"를 기준으로 분리한다.
- `CAP LS 302`와 `005 ISUPPORT`는 현대 IRC 호환성의 최소 신호로 취급하고, TLS나 SASL처럼 일부러 빠진 영역은 마지막 챕터에서 다시 경계로 정리한다.
- 현재 git anchor는 저장소 단위뿐이라, 세부 chronology는 source dependency와 smoke test 시나리오 확장 순서로 복원한다.


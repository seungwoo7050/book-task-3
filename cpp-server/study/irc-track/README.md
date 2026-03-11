# irc-track

## 이 트랙이 푸는 문제

작동하는 IRC subset 서버를 설명할 때 가장 어려운 부분은 등록, room lifecycle, privilege, capstone 확장을 한 번에 섞지 않는 것이다. 이 트랙은 core subset과 capstone을 두 단계로 나눠, 상태 전이와 고급 command를 분리해 읽게 만든다.

## 내가 만든 답

- [01-roomlab](01-roomlab/README.md)에서 registration과 room lifecycle만 먼저 다룬다.
- [02-ircserv](02-ircserv/README.md)에서 `CAP`, `MODE`, `TOPIC`, `INVITE`, `KICK`를 추가해 pure TCP IRC capstone으로 통합한다.

## 포함 lab

| 순서 | lab | 답의 형태 |
| --- | --- | --- |
| 1 | [01-roomlab](01-roomlab/README.md) | registration, JOIN/PART, broadcast smoke test |
| 2 | [02-ircserv](02-ircserv/README.md) | modern IRC capstone과 end-to-end smoke test |

## 읽는 순서

1. [01-roomlab/README.md](01-roomlab/README.md)
2. [02-ircserv/README.md](02-ircserv/README.md)
3. 다른 capstone과 비교하려면 [../game-track/02-arenaserv/README.md](../game-track/02-arenaserv/README.md)

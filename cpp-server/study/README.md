# Study Tracks

`study/`는 이 저장소의 실제 학습 경로다. 지금부터는 lab을 한 줄로 나열하지 않고, 공용 기초와 두 개의 capstone 축으로 나누어 읽는다.

## 트랙 지도

- [shared-core/README.md](shared-core/README.md): event loop와 parser를 먼저 분리해 보는 공용 기초
- [irc-track/README.md](irc-track/README.md): IRC subset 서버를 capstone까지 끌어올리는 축
- [game-track/README.md](game-track/README.md): authoritative simulation에서 TCP game server capstone으로 이어지는 축

## 권장 순서

1. [shared-core/01-eventlab/README.md](shared-core/01-eventlab/README.md)
2. [shared-core/02-msglab/README.md](shared-core/02-msglab/README.md)
3. 전체를 읽는다면 [irc-track/01-roomlab/README.md](irc-track/01-roomlab/README.md) -> [irc-track/02-ircserv/README.md](irc-track/02-ircserv/README.md)
4. 그 다음 [game-track/01-ticklab/README.md](game-track/01-ticklab/README.md) -> [game-track/02-arenaserv/README.md](game-track/02-arenaserv/README.md)

게임 서버 축만 볼 때도 `shared-core`는 먼저 읽는 편이 좋다. `eventlab`의 런타임 기반과 `msglab`의 입력 경계가 뒤쪽 capstone 설명을 훨씬 단순하게 만든다.

## 검증 규칙

- 각 lab의 기본 검증 명령은 해당 `cpp/` 디렉터리에서 `make clean && make test`다.
- 루트 문서는 학습 순서를 설명하고, 실제 명령은 각 lab의 `cpp/README.md`에 둔다.

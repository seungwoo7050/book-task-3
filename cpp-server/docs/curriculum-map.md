# 커리큘럼 맵

## 왜 3트랙 구조로 다시 묶었는가

이 저장소가 풀고 싶은 핵심 문제는 기능 수가 아니라 설명 가능성이다. event loop, parser, IRC 상태 전이, authoritative simulation, capstone을 한 줄로 진열하면 결국 "그래서 어디까지가 어느 문제였는가"가 흐려진다. 그래서 현재 구조는 아래 세 층으로 고정한다.

1. `shared-core`
   - 서버 런타임과 parser 책임을 먼저 분리한다.
2. `irc-track`
   - 연결 위에 IRC 상태 전이를 올리고, 마지막에 capstone으로 다시 통합한다.
3. `game-track`
   - simulation을 headless로 먼저 고정한 뒤, 마지막에 TCP 서버 capstone으로 다시 통합한다.

## 전체 읽기 순서

1. [study/shared-core/01-eventlab](../study/shared-core/01-eventlab/README.md)
2. [study/shared-core/02-msglab](../study/shared-core/02-msglab/README.md)
3. [study/irc-track/01-roomlab](../study/irc-track/01-roomlab/README.md)
4. [study/irc-track/02-ircserv](../study/irc-track/02-ircserv/README.md)
5. [study/game-track/01-ticklab](../study/game-track/01-ticklab/README.md)
6. [study/game-track/02-rollbacklab](../study/game-track/02-rollbacklab/README.md)
7. [study/game-track/03-arenaserv](../study/game-track/03-arenaserv/README.md)

게임 서버 축만 보려면 `shared-core`를 마친 뒤 `game-track`으로 바로 넘어가도 된다. 다만 저장소 전체를 읽을 때는 IRC 축을 먼저 두어 상태 전이와 capstone 통합 패턴을 한 번 더 본 뒤 게임 축으로 넘어가는 편이 설명이 더 잘 맞는다.

## 트랙별 질문

### `shared-core`

- `01-eventlab`: 연결을 받고 읽고 쓰고 정리하는 최소 event loop는 어떻게 움직이는가
- `02-msglab`: parser와 validator를 네트워크 I/O에서 어떻게 분리해야 하는가

### `irc-track`

- `01-roomlab`: 등록과 room lifecycle을 실제 TCP 서버 위에서 어떻게 다룰 것인가
- `02-ircserv`: 앞선 경계를 다시 합쳐 pure TCP IRC capstone을 어디까지 만들 것인가

### `game-track`

- `01-ticklab`: authoritative simulation을 transport 없이 먼저 어떻게 고정할 것인가
- `02-rollbacklab`: late input correction과 rollback replay를 headless로 어떻게 증명할 것인가
- `03-arenaserv`: reconnect와 snapshot을 포함한 최소 authoritative TCP game server를 어떻게 보여 줄 것인가

## 이 구조가 주는 이점

- 학습자가 지금 읽는 코드가 런타임 문제인지 parser 문제인지 상태 전이 문제인지 구분하기 쉽다.
- 각 capstone이 무엇을 새로 더했고 무엇을 일부러 남겼는지 비교하기 쉽다.
- README만 읽어도 문제, 답, 검증 경로가 바로 잡힌다.

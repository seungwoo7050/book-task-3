# cpp-server

이 저장소는 C++ 서버 학습 결과물이 시간이 지나면 "무슨 문제를 풀었고, 어떤 답을 만들었고, 어디까지 검증했는가"가 흐려지는 문제를 다시 정리하기 위해 만든 study-first 레포다.

## 이 레포가 푸는 문제

- 네트워크 서버 학습이 event loop, parser, 상태 전이, capstone을 한 번에 섞어 설명하게 되는 문제
- IRC 서버 축과 authoritative 게임 서버 축이 같은 저장소 안에서 뒤섞여 읽히는 문제
- 학습 레포를 다시 열었을 때 문제, 답, 검증 경로가 앞면에서 바로 보이지 않는 문제

## 내가 만든 답

- `study/`를 `shared-core -> irc-track -> game-track` 3트랙으로 재배치했다.
- 각 lab의 공개 표면을 `README -> problem -> cpp -> docs -> notion` 순서로 고정했다.
- 루트와 각 lab README 첫 화면에서 `푸는 문제 -> 만든 답 -> 검증 방법`이 먼저 보이도록 문서를 다시 썼다.

## 현재 검증 상태

- 기준일: `2026-03-11`
- 아래 6개 lab에서 `make clean && make test`를 다시 실행해 통과를 확인한다.
- 각 lab의 실제 실행 방법은 해당 `cpp/README.md`에 둔다.

| track | lab | 현재 상태 | 검증 진입점 |
| --- | --- | --- | --- |
| `shared-core` | [01-eventlab](study/shared-core/01-eventlab/README.md) | `verified` | [cpp/README.md](study/shared-core/01-eventlab/cpp/README.md) |
| `shared-core` | [02-msglab](study/shared-core/02-msglab/README.md) | `verified` | [cpp/README.md](study/shared-core/02-msglab/cpp/README.md) |
| `irc-track` | [01-roomlab](study/irc-track/01-roomlab/README.md) | `verified` | [cpp/README.md](study/irc-track/01-roomlab/cpp/README.md) |
| `irc-track` | [02-ircserv](study/irc-track/02-ircserv/README.md) | `verified` | [cpp/README.md](study/irc-track/02-ircserv/cpp/README.md) |
| `game-track` | [01-ticklab](study/game-track/01-ticklab/README.md) | `verified` | [cpp/README.md](study/game-track/01-ticklab/cpp/README.md) |
| `game-track` | [02-arenaserv](study/game-track/02-arenaserv/README.md) | `verified` | [cpp/README.md](study/game-track/02-arenaserv/cpp/README.md) |

## 트랙 지도

| track | 포함 lab | 핵심 질문 | capstone |
| --- | --- | --- | --- |
| [shared-core](study/shared-core/README.md) | `01-eventlab`, `02-msglab` | 서버 런타임과 parser 책임을 어디서 끊어 설명할까 | 없음 |
| [irc-track](study/irc-track/README.md) | `01-roomlab`, `02-ircserv` | IRC subset 서버를 어떻게 상태 전이와 capstone으로 확장할까 | `02-ircserv` |
| [game-track](study/game-track/README.md) | `01-ticklab`, `02-arenaserv` | authoritative simulation과 TCP game server를 어떻게 분리해 검증할까 | `02-arenaserv` |

## 먼저 읽을 순서

1. [docs/README.md](docs/README.md)
2. [study/README.md](study/README.md)
3. [study/shared-core/README.md](study/shared-core/README.md)
4. [study/shared-core/01-eventlab/README.md](study/shared-core/01-eventlab/README.md)
5. [study/shared-core/02-msglab/README.md](study/shared-core/02-msglab/README.md)
6. IRC 축이 목적이면 [study/irc-track/README.md](study/irc-track/README.md)부터, 게임 서버 축이 목적이면 [study/game-track/README.md](study/game-track/README.md)부터 이어서 읽는다.

## 기준 문서

- 문서 지도: [docs/README.md](docs/README.md)
- 트랙 설계 이유: [docs/curriculum-map.md](docs/curriculum-map.md)
- 현재 저장소 상태: [docs/repository-audit.md](docs/repository-audit.md)
- 경로 변경표: [docs/path-migration-map.md](docs/path-migration-map.md)

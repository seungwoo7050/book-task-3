# Study Labs

flat `study/` 구조의 C++17 lab 모음이다. IRC server 학습과 game-server 학습이 한 커리큘럼 안에서 만나지만, 각 프로젝트는 독립 과제처럼 읽히고 독립적으로 빌드/테스트된다.

## Labs

| lab | focus |
| --- | --- |
| `eventlab` | non-blocking socket, event loop, keep-alive |
| `msglab` | parser, validation, transcript fixture |
| `roomlab` | session registration, room lifecycle, IRC subset |
| `ticklab` | authoritative fixed-step simulation, snapshot, reconnect grace |
| `ircserv` | pure TCP modern IRC capstone |
| `arenaserv` | pure TCP authoritative party arena capstone |

## Read In This Order

- 저장소 감사: [../docs/repository-audit.md](../docs/repository-audit.md)
- 커리큘럼 맵: [../docs/curriculum-map.md](../docs/curriculum-map.md)
- `eventlab`: [eventlab/README.md](eventlab/README.md)
- `msglab`: [msglab/README.md](msglab/README.md)
- `roomlab`: [roomlab/README.md](roomlab/README.md)
- `ticklab`: [ticklab/README.md](ticklab/README.md)
- `ircserv`: [ircserv/README.md](ircserv/README.md)
- `arenaserv`: [arenaserv/README.md](arenaserv/README.md)

## Verification

- `eventlab/cpp`: `make clean && make && make test`
- `msglab/cpp`: `make clean && make && make test`
- `roomlab/cpp`: `make clean && make && make test`
- `ticklab/cpp`: `make clean && make && make test`
- `ircserv/cpp`: `make clean && make && make test`
- `arenaserv/cpp`: `make clean && make && make test`

`notion/`은 local-only이며 Git에 포함하지 않는다.

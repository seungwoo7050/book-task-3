# cpp-server Study Archive

`legacy/`의 결과물을 읽기 전용으로 보존하고, `study/` 아래에서 C++17 네트워크 서버 커리큘럼으로 다시 세운 저장소다. 현재 목표는 pure IRC 서버와 authoritative game server를 각각 독립적인 capstone으로 갖는 학습 아카이브를 유지하는 것이다.

## What Lives Here

- `legacy/`: 원본 Modern IRC Omok 서버 트리. 게임, WebSocket, 프론트엔드, 저장 계층이 섞여 있으므로 참고 자료로만 읽는다.
- `study/`: flat lab 구조의 활성 학습 트리. 각 프로젝트는 독립 빌드/테스트가 가능해야 한다.
- `docs/`: 저장소 감사, 커리큘럼 맵, 공통 템플릿/상태 규칙.

## Current Labs

1. `eventlab`: non-blocking socket, event loop, keep-alive
2. `msglab`: line framing, parser, validation, transcript fixture
3. `roomlab`: registration, session, room lifecycle가 있는 IRC subset server
4. `ticklab`: authoritative fixed-step match loop, reconnect grace, snapshot correctness
5. `ircserv`: pure TCP modern IRC capstone
6. `arenaserv`: pure TCP authoritative party arena capstone

## Open First

- 학습 경로: [study/README.md](study/README.md)
- 저장소 감사: [docs/repository-audit.md](docs/repository-audit.md)
- 커리큘럼 맵: [docs/curriculum-map.md](docs/curriculum-map.md)
- 템플릿과 상태 규칙: [docs/study-project-template.md](docs/study-project-template.md)

## Notes

- `legacy/`는 수정하지 않는다.
- `notion/`은 local-only 노트이며 Git에 포함하지 않는다.

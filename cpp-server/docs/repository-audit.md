# Repository Audit

기준 점검일: 2026-03-09

## Observed State

- 현재 작업 디렉터리는 Git 메타데이터가 없는 로컬 폴더다.
- `legacy/`는 C++17 IRC 서버 위에 오목, WebSocket, React, Nginx, Docker, MySQL/Redis를 덧붙인 단일 포트폴리오 프로젝트였다.
- 생성물과 문서가 소스 트리와 함께 섞여 있어서, 학습용 project set으로는 읽기 어려웠다.

## Legacy Classification

| 영역 | 경로 예시 | 분류 | 현재 처리 |
| --- | --- | --- | --- |
| 이벤트 루프와 TCP 코어 | `legacy/src/EventManager.*`, `legacy/src/Server.cpp`, `legacy/src/utils.cpp` | solution | `eventlab`, `ircserv`, `arenaserv`의 핵심 구현 근거로 사용 |
| 메시지 모델과 parser | `legacy/src/Message.*`, `legacy/src/Parser.*`, `legacy/src/inc/macros.hpp` | solution | `msglab`, `roomlab`, `ircserv`의 근거로 사용 |
| IRC room lifecycle | `legacy/src/Connection.*`, `legacy/src/Channel.*`, `legacy/src/Executor.*`, `legacy/src/execute_join.cpp` | solution | `roomlab`, `ircserv`의 핵심 reference로 사용 |
| 게임 규칙/운영 확장 | `legacy/src/GameLogic.*`, `legacy/src/GameRoom.*`, `legacy/src/Protocol.*`, `legacy/src/WebSocket.*`, `legacy/web/`, `legacy/nginx/` | solution / ops | 새 `study/`에는 직접 복제하지 않음 |
| 상위 설계 문서 | `legacy/README.md`, `legacy/docs/game-protocol.md`, `legacy/docs/portfolio-checklist.md` | docs | reconstructed problem docs와 capstone 설계의 provenance source로 사용 |
| 발표/회고성 문서 | `legacy/docs/presentation-ko.md`, `legacy/docs/refactor-log.md`, `legacy/dev.log` | notes | public docs로 직접 복제하지 않음 |
| 생성물/노이즈 | `legacy/src/*.o`, `legacy/src/*.d`, `legacy/ircserv`, `legacy/web/dist`, `legacy/web/node_modules` | generated | `study/`로 가져오지 않음 |

## Main Findings

- 레거시 트리는 “하나의 제품”으로는 풍부했지만, “여러 개의 공부 가능한 과제”로는 약했다.
- 순수 네트워크/프로토콜 학습만 복원하면 `eventlab -> msglab -> roomlab -> ircserv`가 자연스럽다.
- 하지만 C++ 게임서버 포지션 포트폴리오를 의식하면 authoritative simulation과 reconnect/snapshot를 별도 bridge와 capstone으로 보여줄 필요가 있다.
- 그래서 flat `study/`는 IRC capstone 하나로 끝나지 않고, `ticklab`와 `arenaserv`를 추가한 6개 lab 구조가 더 적합하다.

## Redesign Decisions

- `legacy/`는 그대로 둔다.
- `study/`는 중간 track 폴더 없이 flat lab 구조를 사용한다.
- lab 셋은 `eventlab`, `msglab`, `roomlab`, `ticklab`, `ircserv`, `arenaserv`로 고정한다.
- `ircserv`는 pure protocol/state-machine capstone이고, `arenaserv`는 authoritative game-server capstone이다.
- WebSocket, React, Docker/Nginx, DB/Redis, metrics는 새 `study/` 공식 커리큘럼에서 제외한다.

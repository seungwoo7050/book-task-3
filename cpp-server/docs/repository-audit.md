# 저장소 감사

기준 점검일: `2026-03-11`

## 현재 확인된 사실

- `study/`는 더 이상 flat lab 목록이 아니라 `shared-core`, `irc-track`, `game-track` 3트랙 구조를 사용한다.
- 각 lab은 `README.md`, `problem/README.md`, `cpp/README.md`, `docs/README.md`, `notion/README.md`, `notion-archive/README.md`를 공개 표면으로 유지한다.
- `notion/`은 현재판 학습 로그이고, `notion-archive/`는 재편 이전 기록과 타임라인 백업이다.
- 구조 변경 이후에도 6개 lab의 기본 검증 명령은 각 `cpp/` 디렉터리에서 `make clean && make test`로 유지한다.

## 이번 패스에서 고친 것

- 문제, 답, 검증 경로가 앞면에서 바로 보이도록 루트와 각 lab README를 재작성했다.
- 상위 경로를 트랙 중심으로 바꾸고, 예전 flat 경로는 [path-migration-map.md](path-migration-map.md)에 모았다.
- `problem/`, `cpp/`, `docs/`, `notion/`의 역할이 서로 겹치지 않도록 문서 층을 다시 나눴다.
- 코드 설명 주석을 한국어 중심으로 다시 맞췄다.

## 현재 커리큘럼이 보여 주는 것

| 축 | 경로 | 최종적으로 보여 주는 역량 |
| --- | --- | --- |
| 공용 기초 | `shared-core/01-eventlab -> shared-core/02-msglab` | event loop, parser, validation, 검증 경계 |
| IRC 서버 | `irc-track/01-roomlab -> irc-track/02-ircserv` | registration, room lifecycle, privilege, IRC capstone |
| 게임 서버 | `game-track/01-ticklab -> game-track/02-arenaserv` | authoritative simulation, reconnect, snapshot, TCP capstone |

## 일부러 하지 않은 것

- lab slug 변경
- 코드 기능 추가
- 운영 배포 범위 확장
- `notion-archive/` 내부의 역사적 경로를 전면 수정하는 일

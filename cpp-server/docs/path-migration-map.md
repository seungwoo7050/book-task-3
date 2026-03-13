# 경로 변경표

이번 구조 개편으로 `study/` 아래의 flat 경로를 트랙 경로로 옮겼다. 예전 경로는 archive 문서 안에 역사적 맥락으로만 남기고, 현재 문서와 검증 명령은 아래 새 경로를 기준으로 읽는다.

| old path | new path | track |
| --- | --- | --- |
| `study/eventlab` | `study/shared-core/01-eventlab` | `shared-core` |
| `study/msglab` | `study/shared-core/02-msglab` | `shared-core` |
| `study/roomlab` | `study/irc-track/01-roomlab` | `irc-track` |
| `study/ircserv` | `study/irc-track/02-ircserv` | `irc-track` |
| `study/ticklab` | `study/game-track/01-ticklab` | `game-track` |
| `study/arenaserv` | `study/game-track/03-arenaserv` | `game-track` |
| 신규 추가 | `study/game-track/02-rollbacklab` | `game-track` |

## 사용 규칙

- 루트 README, 트랙 README, 각 lab README는 모두 새 경로만 사용한다.
- `notion-archive/` 안의 예전 경로 표기는 당시 기록을 보존하기 위한 것이므로 그대로 둔다.
- 경로 이동 이후 검증 명령은 각 lab의 새 `cpp/` 디렉터리에서 실행한다.

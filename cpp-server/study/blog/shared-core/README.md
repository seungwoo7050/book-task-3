# shared-core blog

이 트랙의 blog 시리즈는 event loop와 parser를 capstone에서 떼어 내면 무엇이 더 설명 가능해지는지 프로젝트 단위로 복원한다. chronology는 모두 `source-first` 기준으로 다시 썼고, 공통으로 `problem/README.md`, `cpp/Makefile`, `cpp/src`, `cpp/tests`, `docs/README.md`를 함께 읽는다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| --- | --- | --- |
| eventlab | [README.md](01-eventlab/README.md) | [../../shared-core/01-eventlab/README.md](../../shared-core/01-eventlab/README.md) |
| msglab | [README.md](02-msglab/README.md) | [../../shared-core/02-msglab/README.md](../../shared-core/02-msglab/README.md) |

## 읽는 순서

1. [eventlab](01-eventlab/README.md)로 non-blocking runtime surface를 먼저 본다.
2. [msglab](02-msglab/README.md)로 line framing과 validation 경계를 따로 고정한다.
3. 이후 IRC 축은 [../irc-track/README.md](../irc-track/README.md), 게임 서버 축은 [../game-track/README.md](../game-track/README.md)로 이동한다.

## source-first 메모

- `shared-core`는 기능 추가보다 책임 분리가 중심이므로, chronology도 "무엇을 먼저 떼어 봐야 뒤쪽 capstone이 읽히는가"를 기준으로 쓴다.
- `eventlab`은 `Server`와 `EventManager`의 경계를, `msglab`은 `Message`와 `Parser`의 경계를 핵심 증거로 잡는다.
- 두 lab 모두 git history가 세밀하지 않아 `Day / Session`을 기본 형식으로 쓰고, `2026-03-11`은 현재 검증 표면이 고정된 시점으로만 사용한다.


# cpp-server Source-First Blog

이 디렉터리는 `/Users/woopinbell/work/book-task-3/blog/blog-writing-guide.md` 기준으로 `cpp-server/study`를 다시 읽기 위한 입구다. 목표는 각 lab의 결과만 요약하는 것이 아니라, 소스와 테스트를 따라가며 "무엇을 먼저 만들었고, 어디서 책임을 나눴고, 어떤 검증으로 멈췄는가"를 한 단계씩 복원하는 데 있다.

이번 세트는 기존 초안을 바탕으로 다듬은 글이 아니다. 예전 문서는 [`_legacy/2026-03-13-isolate-and-rewrite/`](_legacy/2026-03-13-isolate-and-rewrite/)로 따로 격리해 두었고, 현재 글은 각 lab의 `README`, `problem/README`, `cpp/README`, 실제 소스, 테스트, 그리고 `make clean && make test` 실행 결과만 근거로 다시 썼다.

읽는 순서는 저장소 구조와 같다. 먼저 `shared-core`에서 런타임과 parser를 분리해 보고, 그 위에 `irc-track`에서 상태 전이와 privilege를 얹고, 마지막으로 `game-track`에서 authoritative simulation과 TCP game server capstone을 본다. 한 축만 먼저 읽어도 되지만, 전체를 따라가면 "무엇을 먼저 떼어 내고, 무엇을 마지막에 다시 합쳤는가"가 더 또렷해진다.

## 트랙 안내

### shared-core

서버의 바닥을 먼저 고정하는 축이다. `eventlab`은 non-blocking runtime을, `msglab`은 line framing과 parser 경계를 분리한다.

- [eventlab](shared-core/01-eventlab/README.md)
- [msglab](shared-core/02-msglab/README.md)

### irc-track

공용 기초 위에 IRC subset을 올리고, 마지막에 advanced command를 포함한 pure TCP capstone으로 확장하는 축이다.

- [roomlab](irc-track/01-roomlab/README.md)
- [ircserv](irc-track/02-ircserv/README.md)

### game-track

먼저 headless authoritative engine을 고정한 뒤, 같은 엔진을 TCP 서버에 연결하는 축이다. runtime보다 simulation을 먼저 분리해 보는 흐름이 중심에 있다.

- [ticklab](game-track/01-ticklab/README.md)
- [rollbacklab](game-track/02-rollbacklab/README.md)
- [arenaserv](game-track/03-arenaserv/README.md)

## 공통 검증 규칙

각 lab의 현재 기준 검증 명령은 해당 `cpp/` 디렉터리에서 아래와 같다.

```sh
make clean && make test
```

본문 글과 evidence ledger는 이 명령의 실제 출력과 테스트 시나리오를 기준으로 정리했다. 그래서 글을 따라가다 궁금해지는 장면이 있으면, 같은 경로에서 같은 명령을 다시 돌려 바로 대조해 볼 수 있다.

# Study Labs

`study/`는 이 저장소의 실제 학습 경로다. IRC 서버 축과 authoritative 게임 서버 축이 한 커리큘럼 안에 들어 있지만, 각 lab은 독립 과제처럼 읽히고 독립적으로 검증된다.

## 읽는 순서

1. [../docs/repository-audit.md](../docs/repository-audit.md)
2. [../docs/curriculum-map.md](../docs/curriculum-map.md)
3. [eventlab/README.md](eventlab/README.md)
4. [msglab/README.md](msglab/README.md)
5. [roomlab/README.md](roomlab/README.md)
6. [ticklab/README.md](ticklab/README.md)
7. [ircserv/README.md](ircserv/README.md)
8. [arenaserv/README.md](arenaserv/README.md)

## lab 요약

| lab | 먼저 배우는 것 | 다음 단계로 이어지는 이유 | 포트폴리오 신호 |
| --- | --- | --- | --- |
| `eventlab` | non-blocking socket, event loop, keep-alive | 이후 모든 서버 lab의 런타임 기반이 된다 | 연결 수명주기 설명, smoke test 로그 |
| `msglab` | parser, validation, transcript test | 네트워크와 parser 책임을 분리하게 해 준다 | 입력 정규화와 테스트 설계 능력 |
| `roomlab` | IRC subset registration, room lifecycle | 상태 전이를 실제 TCP 서버에 올려 본다 | registration과 broadcast 처리 |
| `ticklab` | authoritative fixed-step simulation | 게임 서버 capstone의 핵심 로직을 transport 없이 검증한다 | deterministic simulation, reconnect grace |
| `ircserv` | modern IRC capstone | IRC 축의 완성본이다 | protocol completeness, client compatibility |
| `arenaserv` | authoritative party arena capstone | 게임 서버 축의 완성본이다 | room state machine, snapshot, reconnect |

## 검증 기준

각 lab의 기본 검증 명령은 동일하다.

```sh
make clean && make test
```

2026-03-10 기준으로 6개 lab 모두 이 명령을 다시 확인했다.

## `notion/`과 `notion-archive/`

- `notion/`은 현재 공개용 학습 노트다.
- `notion-archive/`는 예전 초안과 타임라인을 보존하는 백업 폴더다.
- 새로 노트를 다시 쓰더라도 이전 기록을 지우지 않고 축적하는 방식을 기본으로 삼는다.

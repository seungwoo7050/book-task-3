# cpp-server 학습 아카이브

이 저장소는 예전에 만들었던 C++ 서버 작업을 그대로 진열하는 포트폴리오가 아니라, 그 경험을 다시 학습 순서에 맞게 분해해 놓은 공부용 레포다. 목표는 네트워크 서버와 authoritative 게임 서버의 핵심 질문을 단계적으로 익히게 하는 것, 그리고 이 레포를 참고한 학생이 자기만의 더 나은 공개 포트폴리오 레포를 설계할 수 있게 돕는 것이다.

2026-03-10 기준으로 `study/` 아래 6개 lab의 `make clean && make test`를 모두 다시 확인했다. 문서는 이 기준선 위에서 관리한다.

## 여기서 무엇을 볼 수 있는가

- `study/`: 실제 학습 경로다. 각 lab은 독립적으로 읽히고 독립적으로 빌드/테스트된다.
- `docs/`: 이 레포가 왜 이런 순서를 택했는지, 어떤 문서 규칙을 따르는지 설명한다.
- `study/*/notion/`: 현재 공개용 학습 노트다. 친절한 설명과 재정리된 판단 기준을 담는다.
- `study/*/notion-archive/`: 이전 초안과 타임라인을 그대로 보존한 백업 폴더다.

## 학습 순서

1. [study/README.md](study/README.md)에서 전체 순서를 본다.
2. [docs/curriculum-map.md](docs/curriculum-map.md)에서 왜 이 순서가 필요한지 읽는다.
3. 각 lab의 `problem/README.md`로 문제를 먼저 이해한다.
4. `cpp/README.md`로 구현 범위와 검증 명령을 확인한다.
5. `docs/README.md`와 `notion/`으로 사고 과정과 확장 포인트를 따라간다.

## 현재 포함된 lab

| lab | 핵심 질문 | 포트폴리오로 가져갈 수 있는 신호 |
| --- | --- | --- |
| `eventlab` | non-blocking socket과 event loop는 최소 단위에서 어떻게 움직이는가 | 연결 수명주기, keep-alive, smoke test 증거 |
| `msglab` | parser는 네트워크 I/O와 어떻게 분리해야 하는가 | 입력 정규화, validator, transcript 테스트 |
| `roomlab` | IRC subset 서버에서 등록과 room lifecycle은 어떻게 얽히는가 | 상태 전이, broadcast, 중복 nick 처리 |
| `ticklab` | authoritative simulation은 transport 없이도 검증 가능한가 | fixed-step, reconnect grace, deterministic test |
| `ircserv` | 앞선 IRC lab을 합치면 어느 지점이 capstone이 되는가 | protocol completeness, client compatibility |
| `arenaserv` | authoritative game server를 pure TCP로 보여 주려면 무엇이 최소 핵심인가 | session continuity, snapshot, room state machine |

## 문서 원칙

- 현재 레포에 실제로 존재하는 파일만 직접 링크한다.
- `notion/`은 local-only가 아니라 Git에 포함되는 공개용 백업 문서다.
- `notion/`을 새로 쓰고 싶다면 기존 폴더를 `notion-archive/`로 바꿔 보존한 뒤 새 `notion/`을 만든다.
- 공개 문서는 정답 복사용 해설집이 아니라, 학습 흐름과 포트폴리오 설계 판단을 돕는 안내서로 쓴다.

## 먼저 열어볼 문서

- 전체 학습 경로: [study/README.md](study/README.md)
- 저장소 판단 근거: [docs/repository-audit.md](docs/repository-audit.md)
- 커리큘럼 설계 의도: [docs/curriculum-map.md](docs/curriculum-map.md)
- 문서 운영 기준: [docs/README.md](docs/README.md)

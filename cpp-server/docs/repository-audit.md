# 저장소 감사

기준 점검일: 2026-03-10

## 현재 확인된 사실

- 이 디렉터리에는 `legacy/`가 없다. 따라서 문서는 더 이상 존재하지 않는 경로를 전제로 쓰면 안 된다.
- `study/*/notion/`은 이미 Git 추적 대상이다. `notion/`을 local-only로 설명하는 문장은 현재 사실과 어긋난다.
- `eventlab`, `msglab`, `roomlab`, `ticklab`, `ircserv`, `arenaserv`의 `make clean && make test`를 모두 다시 실행했고 통과를 확인했다.
- 학습 경로는 이미 6개 lab으로 나뉘어 있지만, 문서 톤과 provenance 설명은 아직 이전 전제를 많이 끌고 있었다.

## 왜 문서를 다시 써야 했는가

- 존재하지 않는 `legacy/...` 경로가 README와 개념 노트 전반에 남아 있었다.
- `notion/`이 실제로는 공개 백업 문서인데도 local-only처럼 설명되고 있었다.
- 공개 문서가 “무엇을 배우는가”보다 “예전에 무엇이 있었는가”에 더 가까워, 새 학습자가 읽기 어려웠다.
- 개별 lab의 README는 빌드 명령은 알려 주지만, 왜 이 lab을 먼저 읽어야 하는지와 포트폴리오로 어떻게 확장할지에 대한 안내가 약했다.

## 이번 재정의에서 고정한 판단

- 이 레포는 “이전 버전 서버 작업에서 추린 학습 커리큘럼”으로 설명한다. 더 이상 실제 `legacy/` 디렉터리를 전제로 두지 않는다.
- `study/`는 계속 flat 구조를 사용한다. 이번 패스에서는 프로젝트 이름과 순서를 바꾸지 않는다.
- `notion/`은 tracked public backup이다.
- 기존 `notion/`을 다시 쓸 때는 `notion-archive/`로 보존하고, 새 `notion/`은 정리된 5문서 표준으로 다시 만든다.
- 공개 문서는 학생이 자기 포트폴리오 레포를 만들 때 정보 구조를 어떻게 잡아야 하는지까지 안내해야 한다.

## 현재 커리큘럼이 보여 주는 것

| 축 | lab | 최종적으로 보여 주는 역량 |
| --- | --- | --- |
| 네트워크/IRC | `eventlab` → `msglab` → `roomlab` → `ircserv` | event loop, parser, 상태 전이, IRC capstone |
| 게임 서버 | `ticklab` → `arenaserv` | authoritative simulation, reconnect, snapshot, room state machine |

## 이번 패스에서 일부러 하지 않는 것

- 코드 구조 변경
- 프로젝트 순서 변경
- 새로운 lab 추가
- 운영 배포 문서 확장

이번 작업의 목적은 코드를 바꾸는 것이 아니라, 현재 저장소가 이미 가진 학습 가치를 학생이 더 쉽게 꺼내 쓸 수 있게 문서 계약을 다시 맞추는 것이다.

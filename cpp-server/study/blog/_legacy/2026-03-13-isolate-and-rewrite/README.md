# cpp-server study blog

`study/blog/`는 `cpp-server`의 공개 학습 로그 레이어다. 이 디렉터리는 기존 `README.md`와 `docs/`를 대체하지 않고, 각 독립 lab을 실제 소스와 테스트만으로 다시 읽는 `source-first chronology` 시리즈만 모은다.

## 공통 provenance

- 근거 우선순위는 `README.md` -> `problem/README.md` -> `cpp/README.md` -> `cpp/Makefile` -> `cpp/include/inc` -> `cpp/src` -> `cpp/tests` -> `docs/` -> `git log -- cpp-server`다.
- 현재 공개 문서와 구현 표면 밖의 노트 계층은 이 레이어의 근거로 쓰지 않는다.
- 실제 git anchor는 저장소 수준에서만 얇게 남아 있으므로 `2026-03-09`, `2026-03-10`, `2026-03-11` 같은 날짜는 앵커로만 쓰고, 세부 개발 흐름은 `Day / Session`으로 보수적으로 복원한다.
- 재검증 신호는 각 lab README의 `verified` 표면과 test source 안에 직접 적힌 pass 문자열만 사용한다.

## 트랙 카탈로그

| 트랙 | 프로젝트 수 | 시작점 |
| --- | --- | --- |
| [shared-core](shared-core/README.md) | `2` | [eventlab](shared-core/01-eventlab/README.md) |
| [irc-track](irc-track/README.md) | `2` | [roomlab](irc-track/01-roomlab/README.md) |
| [game-track](game-track/README.md) | `2` | [ticklab](game-track/01-ticklab/README.md) |

## 읽는 법

1. 먼저 [../README.md](../README.md)와 원 저장소 [../../README.md](../../README.md)에서 전체 트랙 구조를 확인한다.
2. 원하는 트랙의 blog `README.md`에서 질문과 프로젝트 순서를 잡는다.
3. 각 프로젝트 디렉터리의 `README.md`와 `00-series-map.md`로 source set, canonical CLI, git anchor를 확인한다.
4. 그다음 numbered chronology 파일을 순서대로 읽으며 실제 코드와 테스트가 어떤 판단을 고정하는지 따라간다.

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-09 5721ffb documentation pass on cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

# H-service-boundary-lab 구조 계획

## 문서 목표

이 랩을 "인증과 워크스페이스를 처음 분리하는 순간"으로 읽게 만든다. 독자가 repo 안의 gateway, notification-service, Redis event seam을 먼저 보고 범위를 오해하지 않도록, 문제 정의의 최소 범위와 실제 코드의 확장 흔적을 분리해서 안내한다.

## 중심 논지

현재 검증된 핵심은 두 가지다.

- `identity-service`가 사용자 계약을 담은 access token을 발급한다.
- `workspace-service`가 그 claims만으로 자기 DB 안에서 도메인 흐름을 이어 간다.

이 두 줄이 무너지지 않도록 서술하고, 나머지 요소는 "이미 심어진 다음 경계"로만 배치한다.

## 본문 순서

1. 문제 정의의 범위를 먼저 고정한다.
2. compose 런타임이 실제로 두 서비스만 띄운다는 점을 보여 준다.
3. identity token payload와 workspace claims decode 경로를 연결한다.
4. workspace 도메인 흐름이 자기 DB ownership 안에서 닫히는지 설명한다.
5. outbox, gateway, notification-service를 현재 핵심이 아닌 seam으로 정리한다.
6. 실제 재실행 명령과 성공/실패를 분리해 기록한다.

## 반드시 포함할 근거

- `compose.yaml`의 두 서비스 분리
- identity access token payload
- `workspace-service`의 `get_current_claims()`와 membership 기반 정책
- `create_comment()`의 outbox 적재
- `contracts/README.md`의 notification/event 계약
- `make lint`, `make test`, `make smoke`, `python3 -m pytest tests/test_system.py -q` 재실행 결과

## 반드시 피할 서술

- gateway와 notification-service가 이 랩의 현재 검증 범위에 포함된 것처럼 쓰지 않는다.
- "MSA 전체를 이미 완성했다"는 톤으로 과장하지 않는다.
- 단순한 README 확장판처럼 기능 목록만 늘어놓지 않는다.
- 기존 blog 문장 재활용처럼 보이는 상투적 회고문으로 쓰지 않는다.

## 품질 체크

- chronology가 살아 있는가
- 실제 코드 경계와 문서 경계를 구분했는가
- 검증 명령의 현재 상태를 숨기지 않았는가
- 다음 랩으로 넘어갈 seam을 암시하되 현재 랩의 논지를 흐리지 않았는가

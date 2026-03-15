# K-distributed-ops-lab 구조 계획

## 문서 목표

이 랩을 "운영성 체크리스트"가 아니라 "각 운영 signal이 어떤 질문에 답하는가"를 읽는 문서로 만든다. health, ready, metrics, request correlation, AWS target shape를 한 묶음으로 다루되, 실행된 사실과 가정 문서를 섞지 않는다.

## 중심 논지

현재 검증된 핵심은 네 줄이다.

- 모든 서비스가 health와 metrics surface를 가진다.
- readiness의 의미는 서비스마다 다르다.
- JSON 로그는 `service`와 `request_id`로 최소 correlation을 만든다.
- AWS 문서는 target shape일 뿐, 배포 완료 증거가 아니다.

## 본문 순서

1. 문제 정의에서 운영성 분리 요구를 먼저 고정한다.
2. compose 런타임을 운영 signal 관점으로 다시 읽는다.
3. identity/workspace/notification/gateway의 readiness 차이를 비교한다.
4. 서비스별 metrics가 얼마나 최소한의 기준선인지 설명한다.
5. JSON 로그와 request id를 source-based 근거로 연결한다.
6. AWS 문서의 비-배포성 경계를 명시한다.
7. 실제 재실행 결과를 성공/실패로 기록한다.

## 반드시 포함할 근거

- 각 서비스 `health.py`의 `/live`, `/ready`
- 각 서비스 `ops.py`의 `app_requests_total{service=...}`
- 각 서비스 `core/logging.py`와 `main.py`의 `service`/`request_id` 문맥
- `docs/aws-deployment.md`의 명시적 한계
- `make lint`, `make test`, `make smoke`, `python3 -m pytest tests/test_system.py -q` 재실행 결과

## 반드시 피할 서술

- 모든 `/ready`가 같은 뜻인 것처럼 쓰지 않는다.
- metrics가 이미 풍부한 관측 스택인 것처럼 과장하지 않는다.
- AWS target shape를 실제 운영 완료 상태처럼 쓰지 않는다.
- request correlation을 trace backend 수준으로 과장하지 않는다.

## 품질 체크

- chronology가 살아 있는가
- 각 signal이 답하는 질문이 분명한가
- 실행된 사실과 target-shape 가정이 분리되는가
- 현재 한계와 제외 범위를 숨기지 않았는가

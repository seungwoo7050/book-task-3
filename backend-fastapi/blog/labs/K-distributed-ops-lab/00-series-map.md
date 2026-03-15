# K-distributed-ops-lab 시리즈 맵

이 랩의 주인공은 새 기능이 아니다. 이미 돌아가는 분산 구조를 "운영할 수 있는 형태로 읽는 법"이 핵심이다. `gateway`, `identity-service`, `workspace-service`, `notification-service`가 각각 어떤 health와 metrics를 내고, request id와 JSON 로그가 최소한의 correlation을 어떻게 만들며, AWS 문서는 어디까지 사실이고 어디부터 가정인지 분리해서 본다.

## 이 랩에서 끝까지 붙잡은 질문

- 분산 구조에서 `/health/live`와 `/health/ready`는 왜 같은 의미일 수 없는가
- gateway ready와 내부 서비스 ready는 각각 어떤 질문에 답하는가
- 최소 metrics와 JSON 로그만으로도 무엇을 추적할 수 있는가
- AWS target shape 문서를 "배포 완료"처럼 쓰지 않으려면 어디까지 선을 그어야 하는가

## 이 문서 묶음이 내린 현재 결론

- 모든 서비스가 `live`, `ready`, `metrics` surface를 갖지만 의미는 동일하지 않다.
- `identity-service` ready는 DB 확인, `workspace-service`/`notification-service` ready는 DB+Redis 확인, `gateway` ready는 upstream readiness 집계와 자체 Redis ping을 뜻한다.
- metrics는 모두 `app_requests_total{service="..."}` 한 줄짜리 최소 surface지만, 현재 자동 테스트는 값 증가까지가 아니라 endpoint가 200으로 열리는지까지만 잠근다.
- JSON 로그는 `service`와 `request_id`를 함께 남겨 최소 correlation을 만든다.
- 다만 `request_id`가 실제 로그 레코드마다 어떻게 남는지와 metrics counter가 어떤 요청까지 집계되는지는 이번 검증에서 주로 소스 해석에 기대고, 자동 테스트가 payload까지 직접 잠그지는 않는다.
- `docs/aws-deployment.md`는 target shape 문서일 뿐, 실제 AWS 배포 성공 증거가 아니다.

## 추천 읽기 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-plan.md`

## 각 문서의 역할

- `10-development-timeline.md`: health/ready 분리, metrics, request correlation, target shape 문서의 경계를 시간순으로 정리한다.
- `_evidence-ledger.md`: 각 서비스의 route, logging, 테스트, 명령 재실행 결과를 근거 중심으로 묶는다.
- `_structure-plan.md`: 이 랩을 "운영성 읽기" 문서로 만들기 위한 설명 순서를 남긴다.

## 이번에 다시 확인한 검증 스냅샷

- `make lint`: 통과
- `make test`: 로컬 `python3` 환경에서 gateway 테스트 import 단계에서 `ModuleNotFoundError: No module named 'argon2'`
- `make smoke`: 통과
- `python3 -m pytest tests/test_system.py -q`: 통과

이 랩의 좋은 점은 운영성 이야기를 추상 개념으로 끝내지 않는다는 데 있다. health, metrics, request id, target shape 문서가 모두 코드와 실행 경로에 붙어 있어서, "어떤 신호가 어떤 질문에 답하는가"를 실제 근거와 함께 읽을 수 있다.

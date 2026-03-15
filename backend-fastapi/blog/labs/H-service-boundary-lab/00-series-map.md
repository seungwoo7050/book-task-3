# H-service-boundary-lab 시리즈 맵

이 랩의 출발점은 단순해 보인다. `identity-service`가 토큰을 발급하고, `workspace-service`가 그 claims만으로 workspace를 만든다. 그런데 실제 소스를 열어보면 `gateway`, `notification-service`, Redis 기반 outbox/relay 계약까지 같이 보인다. 그래서 이 문서 묶음은 "문제에서 요구한 첫 서비스 분해가 실제 런타임에서 어디까지 구현됐는가"를 먼저 가르는 데서 시작한다.

## 이 랩에서 끝까지 붙잡은 질문

- 서비스 경계의 최소 단위는 정말 `identity-service`와 `workspace-service` 둘인가
- `workspace-service`는 인증 서비스 DB를 직접 읽지 않고도 도메인 흐름을 유지하는가
- access token claims가 경계 계약으로 충분한가
- 코드 안에 이미 들어와 있는 outbox, gateway, notification 흔적은 현재 랩의 구현으로 봐야 하는가, 다음 seam으로 봐야 하는가

## 이 문서 묶음이 내린 현재 결론

- 검증된 런타임의 중심은 두 서비스 분리와 DB ownership이다.
- top-level compose + system 검증이 직접 잠그는 성공 경로는 "identity가 토큰을 만들고, workspace가 claims만으로 첫 workspace를 만든다"까지다.
- `workspace-service` 안의 membership, invite, project, task, comment, outbox 흐름은 분명히 존재하지만, 이 부분은 한 단계 아래의 service-local integration test가 더 직접적으로 증명한다.
- `gateway`와 `notification-service` 코드는 repo 안에 존재하지만, 이 랩의 `compose.yaml`과 smoke/system 검증 경로에는 올라오지 않는다.
- 다만 `workspace-service` 안에는 `comment.created.v1` outbox와 Redis relay seam이 이미 심어져 있어서, 다음 단계 확장을 예고하는 흔적은 분명하다.

## 추천 읽기 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-plan.md`

## 각 문서의 역할

- `10-development-timeline.md`: 문제 정의, 실제 런타임, claims 경계, outbox seam, 검증 결과를 시간순으로 정리한다.
- `_evidence-ledger.md`: 어떤 파일과 명령으로 무엇을 확인했는지 근거를 모은다.
- `_structure-plan.md`: 이 랩을 "서비스 분리 입문"으로 읽기 위해 어떤 설명 순서를 고정했는지 남긴다.

## 이번에 다시 확인한 검증 스냅샷

- `make lint`: 통과
- `make test`: 로컬 `python3` 환경에서 `identity-service` 테스트 시작 시 `ModuleNotFoundError: No module named 'argon2'`
- `make smoke`: 통과
- `python3 -m pytest tests/test_system.py -q`: 통과

이 랩의 포인트는 화려한 MSA가 아니라 첫 경계 고정이다. 토큰은 인증 서비스가 만들고, 워크스페이스 서비스는 그 토큰의 claims만 믿는다. 그 단순한 규칙이 실제 코드에서 끝까지 유지되는지 추적하는 것이 이 시리즈의 중심이다.

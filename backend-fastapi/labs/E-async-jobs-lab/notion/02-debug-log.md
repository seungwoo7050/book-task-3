# 디버그 로그

## 실패 사례

테스트에서 Celery를 eager mode로 돌리는데도 Redis 연결 에러가 나거나, retry 시도 횟수(`attempt_count`)가 기대보다 적게 기록되는 문제가 있었다.

## 원인

- eager mode라고 해도 broker 설정 자체를 무시하지는 않는다.
- 상태 전이와 시도 횟수 증가 로직이 분리되어 있으면 early return 경로에서 카운트가 빠질 수 있다.

## 수정

- 테스트 환경에서는 broker/backend URL을 `memory://` 계열로 명시적으로 override했다.
- 상태를 바꾸기 전에 `attempt_count`를 먼저 증가시키는 규칙으로 정리했다.

## 검증 근거

- 이 실패는 eager mode와 실제 broker 모드를 같은 것으로 착각하면 테스트가 쉽게 흔들린다는 점을 보여 준다.
- 마지막 기록된 검증은 [../../../docs/verification-report.md](../../../docs/verification-report.md)를 따른다.

## 남은 메모

동시 drain 호출까지 완전히 다루려면 별도 잠금 전략이 필요하지만, 이 랩에서는 확장 주제로 남겨 둔다.

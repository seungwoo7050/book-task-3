# 회고: 비동기가 단순하지 않은 이유

## 잘된 것

**Outbox 패턴의 핵심을 직접 만들었다.**
"job과 event를 같은 트랜잭션에 넣는다"는 말은 쉬운데,
실제로 모델을 정의하고, drain 로직을 짜고, 상태 전이를 테스트하면
그 한 줄이 왜 중요한지 체감할 수 있다.

**Idempotency key가 자연스럽게 들어갔다.**
알림 생성 API에 idempotency key를 넣으니,
클라이언트 재시도가 중복 job을 만들지 않는다는 보장이 코드 수준에서 성립한다.
이것은 HTTP 멱등성을 서버 측에서 구현하는 실용적인 패턴이다.

**Celery eager 모드로 테스트를 격리했다.**
실제 Redis 없이도 워커 로직을 검증할 수 있다는 점이 CI에서 큰 장점이다.
`task_always_eager=True`의 의미와 한계를 모두 경험했다.

## 아쉬운 것

**상태 전이가 `retry@` prefix에 의존한다.**
실제 시스템에서는 외부 응답 코드로 실패를 판단하겠지만,
여기서는 recipient 문자열로 시뮬레이션한다.
학습용으로는 충분하지만, "왜 이런 방식인지" 설명이 필요하다.

**Outbox polling 자동화가 없다.**
drain을 수동으로 호출해야 한다.
cron이나 Celery beat으로 자동 polling하는 구조가 있으면
더 현실적이겠지만, 랩 범위를 넘긴다고 판단했다.

**Worker 프로세스 분리의 경험이 제한적이다.**
compose에서 worker 서비스를 띄우긴 하지만,
실제로 worker가 독립 프로세스로 failure/restart를 겪는 시나리오는 테스트하지 않았다.

## 면접에서 쓸 수 있는 것

- outbox 패턴이 메시지 유실을 방지하는 원리
- idempotency key의 서버 측 구현: key로 기존 record lookup → 없으면 생성
- Celery eager 모드의 의미: 동기 실행이지 설정 무시가 아니다
- attempt_count와 상태 전이를 분리하면 생기는 버그 패턴
- drain 동시성 문제와 비관적 잠금의 필요성

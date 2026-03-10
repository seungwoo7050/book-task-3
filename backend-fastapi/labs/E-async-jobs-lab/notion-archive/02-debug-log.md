# 디버그 기록: Celery eager 모드와 상태 추적

## 문제 1: `task_always_eager` 환경에서 broker 연결 에러

### 증상

`pytest`에서 Celery 태스크를 호출하자 Redis 연결 에러가 발생했다.
테스트 환경에는 Redis가 없는데, broker URL이 `redis://`로 잡혀 있었다.

### 원인

`celery_app.py`가 Settings에서 `celery_broker_url`을 그대로 읽는데,
Settings 기본값이 `memory://`이긴 하지만 `.env` 파일에 redis URL이 있으면
그쪽이 우선한다. `monkeypatch`로 환경 변수를 정리해야 했다.

### 해결

conftest에서 `task_always_eager=True`를 설정하고,
broker/backend URL도 `memory://`로 명시적으로 override했다.
eager 모드에서는 실제 broker를 타지 않으므로 Redis 없이 동작한다.

### 교훈

Celery eager 모드는 "같은 프로세스에서 동기 실행"이라는 뜻이지,
"설정을 무시한다"는 뜻이 아니다.
broker URL validation은 eager=True여도 발생할 수 있다.

## 문제 2: `attempt_count` 불일치

### 증상

retry 시나리오에서 `attempt_count`가 1이어야 할 시점에 0이었다.

### 원인

`process_event`에서 attempt_count를 증가시키기 전에
상태를 먼저 바꾸고 돌아가는 경로가 있었다.
early return 때문에 카운트 증가 로직을 건너뛰었다.

### 해결

상태 전이 로직 안에서 `attempt_count += 1`을 먼저 실행하고,
그 다음에 상태를 결정하도록 순서를 조정했다.

### 교훈

상태 전이와 부수 효과(카운트 증가)가 분리되어 있으면
분기 경로에 따라 누락되기 쉽다.
"전이 전에 항상 카운트부터" 규칙을 정하면 실수가 줄어든다.

## 문제 3: Outbox drain의 멱등성

### 증상

drain을 두 번 연속 호출하면 같은 이벤트가 두 번 처리되는 것처럼 보였다.

### 원인

첫 drain에서 이벤트 status를 `done`으로 바꿨지만,
commit 전에 두 번째 drain 쿼리가 들어오면 아직 `pending`으로 보인다.
테스트 환경에서는 sequential하게 호출하므로 문제없지만,
동시 호출 시나리오에서는 SELECT FOR UPDATE가 필요할 수 있다.

### 해결

현재 랩에서는 단일 drain 호출자를 가정하고,
테스트도 순차적으로 drain을 호출한다.
동시성 보호는 확장 주제로 문서에 남겨 두었다.

### 교훈

outbox drain의 동시성 문제는 비관적 잠금(SELECT FOR UPDATE)이나
advisory lock으로 해결하는 것이 일반적이다.
이 랩에서 직접 구현하지는 않았지만, 면접에서 말할 수 있어야 한다.

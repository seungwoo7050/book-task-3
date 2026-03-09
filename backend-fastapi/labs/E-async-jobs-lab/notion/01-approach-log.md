# 접근 기록: Outbox + Celery를 조립하기까지

## 처음 본 선택지들

비동기 처리를 넣는 방법은 여러 가지가 있었다.

**1) 요청 핸들러 안에서 직접 호출**
가장 간단하지만, 외부 서비스 장애가 곧 API 장애가 된다.
사용자 경험과 시스템 결합도 양쪽에서 나쁘다.

**2) background task (FastAPI built-in)**
`BackgroundTasks`를 쓰면 응답 후에 작업을 돌릴 수 있지만,
프로세스가 죽으면 작업이 사라진다. 재시도 정책도 직접 만들어야 한다.

**3) Outbox + Celery worker**
job과 outbox event를 같은 트랜잭션에 기록 → drain 시점에 Celery로 위임.
메시지 유실이 구조적으로 방지되고, retry를 worker 쪽에서 처리할 수 있다.

세 번째 방식이 학습 가치가 가장 높다고 판단했다.

## 핵심 설계 결정

### Idempotency Key

`POST /notifications`에 `Idempotency-Key` 헤더를 필수로 둔다.
서비스 레이어에서 같은 key의 기존 job이 있으면 그것을 돌려주고,
없으면 새 `NotificationJob`과 `OutboxEvent`를 같은 세션에서 만든다.
이 둘이 하나의 트랜잭션에 들어가는 것이 outbox 패턴의 핵심이다.

### 상태 전이 모델

```
pending → retrying → sent
```

- `enqueue_notification` 시점: job=`pending`, outbox event=`pending`
- 첫 drain에서 `retry@`로 시작하는 recipient이면: job=`retrying`, attempt_count 증가
- 두 번째 drain: job=`sent`, attempt_count 재증가

`retry@` prefix는 실제 실패를 시뮬레이션하기 위한 테스트 규약이다.
프로덕션에서는 외부 서비스 응답 코드로 판단하겠지만,
이 랩에서는 상태 머신 자체를 검증하는 데 집중한다.

### Outbox Event의 역할

`OutboxEvent`는 `NotificationJob`과 1:1 FK 관계를 맺는다.
drain이 호출되면 `pending` 상태의 이벤트를 꺼내 `process_event`를 실행하고,
처리 후 이벤트 상태를 `done`으로 바꾼다.
이렇게 하면 "어떤 job이 아직 worker에게 전달되지 않았는가"를 항상 알 수 있다.

### Celery 설정

- broker: `memory://` (테스트), `redis://` (compose)
- result backend: `cache+memory://` (테스트)
- `task_always_eager`: 테스트에서만 True로 설정해 동기 실행

`celery_app.py`에서 FastAPI 설정을 읽어오고,
`tasks.py`에 `deliver_notification` 태스크를 정의했다.

## 버린 아이디어

- FastAPI `BackgroundTasks`만으로 처리하는 방식은
  재시도와 영속성이 모두 약해서 제외했다.
- RabbitMQ를 broker로 쓰는 방식은 이미 Redis가 스택에 있으므로
  인프라 복잡도만 올라간다고 판단했다.
- outbox polling을 cron으로 자동화하는 것은 범위 밖으로 남겼다.

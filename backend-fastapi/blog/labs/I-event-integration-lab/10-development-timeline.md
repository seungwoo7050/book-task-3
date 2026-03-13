# I-event-integration-lab 개발 타임라인

## 2026-03-10
### Session 1

- 목표: H에서 workspace-service와 identity-service를 분리했다. 이제 "알림을 보내야 하는데, 같은 DB에 있지 않다"는 문제가 생겼다. 처음엔 "workspace-service에서 직접 알림을 보내면 되지 않나?"라고 생각했다.
- 진행: 하지만 그러면 workspace-service가 알림 발송까지 책임지게 된다. 알림 서비스가 다운되면 댓글 저장도 실패한다. 저장과 전달을 분리해야 한다.
- 판단: E-async-jobs-lab에서 배운 outbox 패턴을 서비스 경계로 옮기기로 했다. workspace-service는 댓글을 저장하면서 outbox에 이벤트를 적재하고, notification-service가 그 이벤트를 소비한다.

CLI:

```bash
$ cd labs/I-event-integration-lab/fastapi
$ make install
```

### Session 2

- 목표: outbox relay와 consume 경로를 구현한다.
- 진행: workspace-service 쪽에 `/events/relay`와 `/debug/outbox/pending` route를 만들었다. relay가 호출되면 pending 이벤트를 Redis Streams로 보내고, notification-service의 `/consume`이 그걸 읽는다.
- 이슈: 처음엔 relay를 주기적으로 자동 실행하려 했다. 하지만 이 랩에서는 "relay가 언제 불리는지"를 관찰 가능하게 만드는 것이 더 중요하다. 명시적 API 호출로 남겼다.

```python
@router.post("/events/relay", response_model=dict[str, int])
def relay_outbox(service: Annotated[WorkspaceService, Depends(get_workspace_service)]) -> dict[str, int]:
    return {"relayed": service.relay_outbox()}

@router.get("/debug/outbox/pending", response_model=dict[str, int])
def pending_outbox(service: Annotated[WorkspaceService, Depends(get_workspace_service)]) -> dict[str, int]:
    return {"pending": service.pending_outbox()}
```

이 route 두 개 덕분에 "댓글을 저장했지만 아직 relay하지 않은 상태"를 관찰할 수 있다. 저장과 전달 사이에 실제로 중간 상태가 존재한다는 걸 눈으로 확인하는 것이 이 랩의 목적이다.

### Session 3

- 목표: notification-service의 idempotent consumer를 구현한다.
- 진행: consume은 처리한 이벤트 수를 반환한다.
- 이슈: 같은 이벤트가 두 번 consume되면 알림이 두 번 가야 하나? 처음엔 "그냥 처리하면 되지"라고 생각했는데, 네트워크 재시도로 같은 이벤트가 중복 도착할 수 있다.
- 조치: 이미 처리한 이벤트는 다시 처리하지 않는 idempotent consumer를 만들었다.

```python
@router.post("/consume", response_model=dict[str, int])
def consume(service: Annotated[NotificationService, Depends(get_notification_service)]) -> dict[str, int]:
    return {"processed": service.consume()}
```

테스트에서 첫 consume 후 `processed == 1`, 두 번째 consume 후 `processed == 0`을 확인한다. 두 번째 호출에서 0이 나온다는 건, 같은 이벤트를 다시 처리하지 않았다는 뜻이다.

```python
first_consume = notifications.post("/internal/notifications/consume")
second_consume = notifications.post("/internal/notifications/consume")
assert first_consume.json()["processed"] == 1
assert second_consume.json()["processed"] == 0
```

나중에 보니 이 두 줄이 이 랩의 핵심 증거다. eventual consistency에서 "최소 한 번 전달"과 "정확히 한 번 처리"의 차이가 여기에 있다.

### Session 4

- 목표: 전체 시스템 흐름을 system test로 묶고 검증한다.
- 진행: owner가 workspace → invite → project → task → comment를 만들고, outbox pending이 1이 되는지 확인하고, relay → consume → 알림 저장까지 전체 경로를 하나의 테스트에 넣었다.
- 이슈: system test 작성 중 토큰 생성 문제가 있었다. H와 달리 이 랩에서는 identity-service를 올리지 않고 JWT를 직접 만들어야 했다. 테스트 안에서 `_token()` 헬퍼를 만들어 해결.
- 검증: lint, test, smoke 모두 통과.
- 다음: 이 랩은 outbox와 consumer까지만 잡고, public API를 유지하면서 이 내부 경계를 감추는 gateway는 J-edge-gateway-lab으로 넘긴다.

CLI:

```bash
$ python -m pytest tests/test_system.py -q
```

```
1 passed
```

```bash
$ make lint
$ make test
$ make smoke
$ docker compose up --build
```

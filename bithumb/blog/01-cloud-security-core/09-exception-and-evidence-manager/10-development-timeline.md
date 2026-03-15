# 09 Exception and Evidence Manager: 억제보다 먼저 남겨야 하는 기록들

보안 운영에서 예외는 보통 "알람을 잠깐 꺼 둔다"는 감각으로 소비되기 쉽다. 그런데 실제 거버넌스 관점에서는 그보다 먼저 남겨야 할 것이 많다. 왜 허용했는지, 누가 승인했는지, 언제 만료되는지, 어떤 증빙이 붙었는지, 그리고 그 모든 변화가 어떤 순서로 일어났는지다. 이 lab은 바로 그 최소 모델을 메모리 안에서 먼저 만든다.

## 구현 순서 요약
1. exception, evidence, audit를 각각 별도 record로 분리했다.
2. approval과 expiry를 suppression 판정에 연결했다.
3. append-only audit와 현재 key semantics의 한계를 함께 드러냈다.

## Phase 1. 예외를 mute가 아니라 record로 만들었다

`manager.py`를 열면 가장 먼저 눈에 들어오는 것은 `ExceptionRecord`, `Evidence`, `AuditEvent` 세 dataclass다. 이건 꽤 중요한 선택이다. 예외를 bool 하나로 표현하면 "왜", "누가", "언제까지", "무슨 근거로"를 담을 곳이 없다. 그래서 이 lab은 suppression 로직보다 먼저 record 경계를 쪼갠다.

CLI demo도 이 구조를 그대로 보여 준다. 예외를 하나 만들고, 승인하고, 증적을 하나 붙이면 출력은 단순 성공 메시지가 아니라 `exception_id`, `approved_status`, `evidence_id`, `audit_event_count`를 JSON으로 보여 준다. 즉 이 lab의 첫 산출물은 억제 여부보다 governance record 집합이다.

재실행:

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m exception_evidence_manager.cli
```

확인한 출력 핵심:
- `approved_status`: `approved`
- `audit_event_count`: `3`

create, approve, append evidence 세 단계가 모두 별도 기록이라는 뜻이다.

## Phase 2. suppression은 예외 존재가 아니라 승인 + 미만료 상태다

다음으로 중요한 건 언제 suppression이 실제로 성립하느냐였다. `create_exception()`이 만든 record는 처음엔 `pending`이다. `approve_exception()`을 거쳐야만 `approved`가 되고, `is_suppressed()`는 여기에 더해 `expires_at > now` 조건까지 만족해야 `True`를 준다.

즉 이 모델은 예외가 있다고 해서 곧바로 finding을 누르지 않는다. 승인되었고 아직 살아 있는 예외만 suppression으로 친다. 이번 보조 재실행에서도 그 차이를 직접 확인했다.

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python - <<'PY'
from exception_evidence_manager.manager import ExceptionManager

m = ExceptionManager()
r = m.create_exception('finding', 'shared-1', 'temp exception', 7)
print('pending_suppressed', m.is_suppressed('shared-1'))
m.approve_exception(r.id, 'security.manager')
print('approved_suppressed', m.is_suppressed('shared-1'))
PY
```

출력은 이렇게 나왔다.

- `pending_suppressed False`
- `approved_suppressed True`

그리고 pytest는 만료 이후엔 다시 `False`가 되어야 한다는 점까지 같이 잠가 둔다.

## Phase 3. audit는 append-only지만, suppression key는 아직 단순하다

마지막으로 본 것은 이 모델이 어디까지 정교한가였다. 좋은 쪽부터 보면 audit trail은 단순하고 분명하다. `create_exception()`은 `exception.created`, `approve_exception()`은 `exception.approved`, `append_evidence()`는 `evidence.added`를 계속 list 뒤에 붙인다. 그래서 변화 순서를 복원하기 쉽다.

하지만 보조 재실행을 해 보니 현재 key semantics는 꽤 단순하다. `is_suppressed()`는 `scope_type`을 보지 않고 `scope_id`만 비교한다. 실제로 `scope_type='finding'`과 `scope_type='image'`를 다르게 두고, 둘 다 `scope_id='shared-1'`로 만든 뒤 승인해도 suppression 판정은 그냥 `shared-1` 하나로 묶여 버린다.

이 결과는 지금 단계에선 이해할 만하다. 이 lab의 목표는 DB 스키마 완성이 아니라 최소 governance flow이기 때문이다. 그래도 capstone으로 넘어갈 때 확장해야 할 지점이 어디인지 분명히 보여 준다.

또 하나 눈에 띄는 점은 evidence audit의 `entity_id`다. evidence record 자체의 ID가 아니라 finding ID를 쓴다. 그래서 "이 finding에 증적이 붙었다"는 사실은 남지만, 특정 evidence 레코드를 중심으로 감사 이력을 추적하는 모델은 아직 아니다.

## 검증

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m pytest \
/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

```text
..                                                                       [100%]
2 passed in 0.01s
```

이 테스트 셋은 작지만 중요한 경계를 잠근다. 승인 전엔 억제되지 않고, 승인 후 만료 전까지만 억제되며, create/approve/evidence append 세 단계가 audit count `3`으로 남아야 한다.

## 지금 상태에서 분명한 한계

- 메모리 모델이라 영속화가 없다.
- suppression key가 `scope_id` 단일 축이라 세밀한 scope partition이 어렵다.
- revoke, renew, evidence removal 같은 후속 동작은 없다.
- approver와 evidence identity가 더 풍부한 governance system으로는 아직 확장 전 단계다.

그래도 이 lab이 중요한 이유는 분명하다. finding 이후 운영을 "무시 처리"로 단순화하지 않고, record와 시간과 근거의 문제로 다시 정의하기 때문이다. capstone DB 모델이 커질 때도 결국 여기서 나눈 경계들을 그대로 가져가게 된다.

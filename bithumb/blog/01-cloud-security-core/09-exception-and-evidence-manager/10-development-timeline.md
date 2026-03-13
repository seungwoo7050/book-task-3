# 10 Development Timeline

이 문서는 `Exception and Evidence Manager`를 현재 메모리 모델과 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 finding mute 토글이 아니라, 예외와 증적을 별도 관리 대상으로 나누는 모델인지 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `manager.py`, `test_manager.py`를 읽었다.
- 이슈: 처음엔 승인된 예외 하나만 있으면 suppression이 끝난다고 생각했는데, 실제 테스트는 expiry와 audit event 개수까지 함께 고정하고 있었다.
- 판단: 이 프로젝트의 중심은 `is_suppressed()` boolean보다, 그 boolean이 어떤 레코드와 이벤트 이력 위에서 계산되는지 보여 주는 데 있다.

CLI:

```bash
$ sed -n '1,120p' 01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md
$ sed -n '1,240p' 01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py
$ sed -n '1,200p' 01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py
```

이 시점의 핵심 코드는 suppression을 승인 상태와 만료 시각으로 계산하는 부분이었다.

```python
        return any(
            record.scope_id == scope_id
            and record.status == "approved"
            and record.expires_at > current
            for record in self.exceptions.values()
        )
```

처음엔 exception 존재 여부만 보면 된다고 생각했지만, 나중에 보니 `approved`와 `expires_at`이 빠지면 suppression이 운영 모델이 아니라 단순 mute가 된다. 이 짧은 predicate가 프로젝트 전체의 의도를 가장 명확하게 드러낸다.

### Session 2

- 진행: demo CLI와 pytest를 돌려 audit event 개수와 expiry 동작이 현재도 유지되는지 확인했다.
- 검증: CLI는 `approved_status: approved`, `audit_event_count: 3`을 출력했고, pytest는 suppression 만료와 append-only audit 경로 두 테스트를 통과했다.
- 판단: 처음 가설은 evidence만 남기면 충분하다는 쪽이었지만, `exception.created -> exception.approved -> evidence.added` 세 이벤트가 따로 남아야 이후 capstone DB에서도 흐름을 재구성할 수 있다.
- 다음: 10번 capstone은 이 메모리 모델을 SQLAlchemy row와 suppression overlay로 다시 옮긴다.

CLI:

```bash
$ make venv
$ PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli
$ PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

출력:

```text
"approved_status": "approved"
"audit_event_count": 3
2 passed in 0.01s
```

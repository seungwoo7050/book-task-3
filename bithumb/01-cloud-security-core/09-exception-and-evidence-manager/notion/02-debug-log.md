# 디버그 로그

## 실제로 자주 막히는 지점

- archive의 예전 설명과 달리 현재 구현은 `scope_type`, `scope_id`, `days`를 기준으로 예외를 만듭니다. 문서와 현재 코드를 섞어 읽지 않도록 주의해야 합니다.
- suppression은 예외 존재 여부만으로 결정되지 않습니다. `approved` 상태이면서 `expires_at > now`여야 합니다.
- evidence와 audit event는 서로 다른 리스트입니다. evidence를 append했다고 suppression 상태가 바뀌지는 않습니다.

## 이미 확인된 테스트 시나리오

- `test_exception_suppresses_scope_until_expiry`: 승인 후 suppression이 켜지고, 미래 시점에서는 만료로 꺼지는지 확인합니다.
- `test_evidence_and_audit_events_are_appended`: 증거 추가와 audit event append가 모두 남는지 검증합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_manager.py](../python/tests/test_manager.py)
- 구현 진입점: [../python/src/exception_evidence_manager/manager.py](../python/src/exception_evidence_manager/manager.py)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

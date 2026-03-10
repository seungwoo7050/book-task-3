# 디버그 로그

## 실제로 자주 막히는 지점

- `finding_id` 필드 이름과 실제 plan이 가리키는 대상(`resource_id`)이 헷갈릴 수 있습니다. 현재 구현은 `resource_id`를 plan의 식별자로 사용합니다.
- `CSPM-001`과 `CSPM-002`는 둘 다 승인 전 상태로 시작하지만, 사람이 개입해야 하는 정도가 다릅니다.
- 승인 함수는 기존 plan을 mutate하지 않고 새 인스턴스를 반환합니다. 이 점을 놓치면 상태 전이 설명이 흐려집니다.

## 이미 확인된 테스트 시나리오

- `test_build_dry_run_returns_patch_for_public_access_finding`: auto patch 모드와 patch 내용, `pending_approval` 상태를 함께 검증합니다.
- `test_approve_marks_plan_approved`: 승인 후 상태와 summary의 승인자 반영을 확인합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_runner.py](../python/tests/test_runner.py)
- 구현 진입점: [../python/src/remediation_pack_runner/runner.py](../python/src/remediation_pack_runner/runner.py)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

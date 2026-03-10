# 재현 가이드

## 무엇을 재현하나

- sample finding이 실제 dry-run remediation plan으로 변환되는지
- plan 상태가 승인 전 `pending_approval`, 승인 후 `approved`로 바뀌는지
- patch 초안이 control_id 맥락과 일치하는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli dry-run 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

## 기대 결과

- CLI JSON에는 `mode: auto_patch_available`, `status: pending_approval`가 포함돼야 합니다.
- `commands_or_patch` 배열 안에는 `block_public_acls`를 포함한 patch 초안이 있어야 합니다.
- pytest는 2개 테스트를 통과하면서 build_dry_run과 approve 두 단계를 모두 검증해야 합니다.

## 결과가 다르면 먼저 볼 파일

- 조치안 생성 규칙을 다시 보려면: [../python/src/remediation_pack_runner/runner.py](../python/src/remediation_pack_runner/runner.py)
- CLI 진입 흐름을 다시 보려면: [../python/src/remediation_pack_runner/cli.py](../python/src/remediation_pack_runner/cli.py)
- 샘플 입력을 다시 보려면: [../problem/data/sample_finding.json](../problem/data/sample_finding.json)
- 검증 기준을 다시 보려면: [../python/tests/test_runner.py](../python/tests/test_runner.py)
- 루트 공통 검증 흐름을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 finding 이후 단계에서도 설계 판단이 많고, 안전한 자동화는 승인과 상태 전이를 먼저 모델링해야 한다는 점을 보여 줍니다.
- 학습자는 여기서 “고친다”보다 “검토 가능한 조치안을 만든다”는 표현을 정확히 이해하는 것이 중요합니다.

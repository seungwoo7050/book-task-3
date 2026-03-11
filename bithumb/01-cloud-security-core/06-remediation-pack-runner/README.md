# 06 Remediation Pack Runner

## 풀려는 문제

finding이 나왔다고 해서 곧바로 patch를 적용하면 운영 리스크가 커집니다.
이 프로젝트는 탐지 이후 단계를 `실행`이 아니라 `검토 가능한 조치안 제안`으로 바꾸는 것을 목표로 합니다.

## 내가 낸 답

- finding JSON을 remediation plan으로 변환합니다.
- `auto_patch_available`, `manual_approval_required`, `manual_review` 같은 운영 모드를 분리합니다.
- 실제 적용 대신 사람이 검토할 수 있는 patch/command 초안을 반환합니다.
- 승인 전후 상태를 분리해 이후 control plane worker가 재사용할 수 있게 합니다.

## 입력과 출력

- 입력: `problem/data/sample_finding.json`
- 출력: remediation mode, 요약, patch 초안, 승인 필요 상태

## 검증 방법

```bash
make venv
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

## 현재 상태

- `verified`
- dry-run remediation 제안과 승인 상태 전이를 fixture로 재현할 수 있습니다.
- 10번 캡스톤의 remediation worker가 이 출력 구조를 그대로 사용합니다.

## 한계와 다음 단계

- 실제 apply와 rollback orchestration은 하지 않습니다.
- 외부 승인 시스템 연동은 없고, 학습용 상태 전이 모델까지만 제공합니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)

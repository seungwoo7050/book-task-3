# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- finding 입력을 remediation plan으로 변환합니다.
- dry-run 중심의 제안과 approval 흐름을 구분합니다.
- 실행 가능한 패치가 아니라 검토 가능한 제안 문서를 만듭니다.

## 핵심 엔트리포인트

- `python/src/remediation_pack_runner/runner.py`
- `python/src/remediation_pack_runner/cli.py`

## 실행

```bash
make venv
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

## 대표 출력 예시

```json
{
  "finding_id": "study2-public-logs",
  "mode": "auto_patch_available",
  "summary": "Enable all public access block flags for the bucket.",
  "status": "pending_approval"
}
```

## 구현 메모

runner는 작은 finding JSON을 입력받아 사람이 읽을 수 있는 조치 계획으로 바꾸는 데 집중합니다.

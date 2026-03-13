# 10 Development Timeline

이 문서는 `Remediation Pack Runner`를 현재 sample finding, runner 코드, 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 자동 수정보다 “검토 가능한 제안”을 우선한다는 점을 실제 소스에서 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `runner.py`, `test_runner.py`를 읽었다.
- 이슈: 처음엔 remediation 프로젝트면 곧바로 patch를 적용하는 흐름까지 있을 거라 예상했지만, 실제 구현은 `pending_approval`을 기본 상태로 두고 있었다.
- 판단: 이 프로젝트의 역할은 인프라 변경기가 아니라, finding을 사람이 검토할 수 있는 change proposal로 바꾸는 것이다.

CLI:

```bash
$ sed -n '1,120p' 01-cloud-security-core/06-remediation-pack-runner/problem/README.md
$ sed -n '1,220p' 01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py
$ sed -n '1,160p' 01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py
```

이 시점의 핵심 코드는 `control_id`에 따라 mode와 patch 모양을 바꾸는 부분이었다.

```python
    if control_id == "CSPM-001":
        return RemediationPlan(... mode="auto_patch_available", status="pending_approval")
    if control_id == "CSPM-002":
        return RemediationPlan(... mode="manual_approval_required", status="pending_approval")
```

처음엔 모든 finding을 `manual_review`로 뭉개도 된다고 생각했지만, 실제로는 S3 public access block처럼 patch 초안이 분명한 케이스와 SSH/RDP 개방처럼 운영 승인 맥락이 필요한 케이스를 나눠야 한다. 이 분기 덕분에 “바로 고쳐도 되는가”와 “사람이 먼저 봐야 하는가”를 출력에서 바로 설명할 수 있다.

### Session 2

- 진행: CLI와 pytest를 다시 돌려 patch 초안과 승인 상태 전환이 현재도 유지되는지 확인했다.
- 검증: CLI는 `auto_patch_available`, `pending_approval`을 포함한 remediation JSON을 출력했고, pytest는 patch 생성과 approval 두 테스트를 통과했다.
- 판단: 처음 가설은 approval이 별도 객체여야 한다는 쪽이었지만, 이 프로젝트 범위에서는 같은 plan을 새 summary/status로 재작성하는 편이 더 단순하고 이후 capstone에 옮기기도 쉬웠다.
- 다음: 10번 capstone의 remediation worker는 여기서 만든 mode 구분을 거의 그대로 재사용한다.

CLI:

```bash
$ make venv
$ PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
$ PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

출력:

```text
"mode": "auto_patch_available"
"status": "pending_approval"
2 passed in 0.01s
```

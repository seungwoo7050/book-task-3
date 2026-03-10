# 디버그 로그

## 실제로 자주 막히는 지점

- S3 public access는 네 플래그를 함께 봐야 합니다. 하나라도 `false`면 위험하다는 점을 놓치기 쉽습니다.
- open ingress는 포트와 CIDR을 같이 봐야 합니다. 22/3389 포트 + `0.0.0.0/0` 조합이 핵심입니다.
- access key age는 plan JSON에 없으므로, plan만 보고 CSPM을 다 설명하려 하면 범위가 좁아집니다.

## 이미 확인된 테스트 시나리오

- `test_insecure_plan_reports_expected_findings`: `CSPM-001`, `CSPM-002`, `CSPM-003` 조합이 정확히 나오는지 확인합니다.
- `test_secure_plan_reports_no_findings`: secure fixture에서 0건이 나오는지 확인합니다.
- `test_access_key_snapshot_reports_old_key`: 120일 key만 `CSPM-004`로 잡히는지 확인합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 구현 진입점: [../python/src/cspm_rule_engine/scanner.py](../python/src/cspm_rule_engine/scanner.py)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

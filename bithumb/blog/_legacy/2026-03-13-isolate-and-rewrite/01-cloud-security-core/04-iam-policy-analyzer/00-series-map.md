# 04 IAM Policy Analyzer - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `analyzer.py`, `cli.py`, `test_analyzer.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- allow/deny 결과를 넘어서, policy가 왜 위험한지 어떤 finding으로 설명할 수 있을까
- broad admin과 `iam:PassRole`을 같은 위험으로 뭉개지 않고 분리하려면 어떤 규칙이 필요할까

## 실제 구현 표면

- `*` action, `*` resource, privilege escalation action을 각각 별도 control ID로 변환합니다.
- finding은 `source`, `control_id`, `severity`, `resource_id`, `evidence_ref`를 포함한 작은 JSON 배열로 반환됩니다.
- `scoped_policy.json`이 0건이어야 한다는 기준선이 함께 고정돼 있습니다.

## 대표 검증 엔트리

- `PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json`
- `PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../01-cloud-security-core/04-iam-policy-analyzer/README.md)
2. [문제 정의](../../../01-cloud-security-core/04-iam-policy-analyzer/problem/README.md)
3. [실행 진입점](../../../01-cloud-security-core/04-iam-policy-analyzer/python/README.md)
4. [대표 테스트](../../../01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py)
5. [핵심 구현](../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../01-cloud-security-core/04-iam-policy-analyzer/README.md)
- [problem/README.md](../../../01-cloud-security-core/04-iam-policy-analyzer/problem/README.md)
- [python/README.md](../../../01-cloud-security-core/04-iam-policy-analyzer/python/README.md)
- [analyzer.py](../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py)
- [cli.py](../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/cli.py)
- [test_analyzer.py](../../../01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

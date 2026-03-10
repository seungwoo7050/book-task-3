# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 다루는 범위

- broad admin과 scoped policy를 구분합니다.
- `iam:PassRole` 같은 escalation action을 별도 고위험 finding으로 분리합니다.
- 설명 가능한 finding 구조와 severity를 반환합니다.

## 실행 예시

```bash
make venv
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
```

## 테스트

```bash
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## 상태

`verified`

## 구현 메모

분석기는 policy JSON을 읽고 즉시 finding을 반환하는 작은 CLI라서 캡스톤에 재사용하기 쉽습니다.

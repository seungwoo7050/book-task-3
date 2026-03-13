# 04 IAM Policy Analyzer 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- foundation의 allow/deny 설명 계층을 “risk finding”으로 다시 해석하는 전환점을 보여 준다.
- 글은 `finding shape -> broad permission 분해 -> escalation/false positive 경계`로 이어지게 배치한다.

## 먼저 붙들 소스 묶음
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/README.md`](../../../01-cloud-security-core/04-iam-policy-analyzer/README.md)
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/problem/README.md`](../../../01-cloud-security-core/04-iam-policy-analyzer/problem/README.md)
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/docs/concepts/least-privilege-findings.md`](../../../01-cloud-security-core/04-iam-policy-analyzer/docs/concepts/least-privilege-findings.md)
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/python/README.md`](../../../01-cloud-security-core/04-iam-policy-analyzer/python/README.md)
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py`](../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py)
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/cli.py`](../../../01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/cli.py)
- [`../../../01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py`](../../../01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - least privilege finding이 어떤 질문을 추가하는지와 canonical verify를 먼저 세운다.
- `10-development-timeline.md`
  - 도입: 허용/거부 판단을 그대로 보여 주는 것만으로는 왜 위험한지 말할 수 없다는 점에서 시작한다.
  - Phase 1. finding 스키마를 먼저 고정했다.
  - Phase 2. broad admin을 두 control로 분해했다.
  - Phase 3. escalation action과 false positive 경계를 함께 고정했다.
  - 마무리: remediation이 이 finding shape를 어떻게 이어받는지 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: `Finding` dataclass, wildcard broad permission check, `iam:PassRole` escalation rule, scoped policy 0건 테스트
- CLI 앵커: `python -m iam_policy_analyzer.cli ...`, `pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests`
- 개념 훅: least privilege 분석은 “허용 여부”가 아니라 “운영상 어떤 질문이 추가로 생기는가”를 control 단위로 분해하는 일이라는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.

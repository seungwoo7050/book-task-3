# Least Privilege Findings

- broad admin은 `Action=*`와 `Resource=*` 두 축으로 나눠 보는 편이 remediation에 유리하다.
- `iam:PassRole`, `CreatePolicyVersion` 같은 escalation action은 별도 high-risk control로 다루는 게 좋다.


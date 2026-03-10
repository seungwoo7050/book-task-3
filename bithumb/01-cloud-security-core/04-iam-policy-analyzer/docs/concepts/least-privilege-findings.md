# Least Privilege Finding 설계

- broad admin은 `Action=*`와 `Resource=*`를 분리해 보는 편이 remediation에 유리합니다.
- `iam:PassRole`, `CreatePolicyVersion` 같은 escalation action은 별도 고위험 control로 다루는 편이 좋습니다.
- 읽기 전용이거나 범위가 충분히 좁은 정책은 불필요한 finding으로 만들지 않는 것이 중요합니다.

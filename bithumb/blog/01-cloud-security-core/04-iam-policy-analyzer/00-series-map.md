# 04 IAM Policy Analyzer series map

이 시리즈는 `04-iam-policy-analyzer`를 단순 policy lint가 아니라, foundation의 allow/deny 감각을 triage 가능한 least-privilege finding으로 바꾸는 첫 규칙 엔진으로 읽는다. 실제 구현은 broad action(`IAM-001`), broad resource(`IAM-002`), privilege escalation action(`IAM-003`)을 분리해 finding 배열로 돌려준다. 반대로 `Condition`, permission boundary, SCP, `s3:*` 같은 wildcard family 전체 해석은 아직 하지 않는다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   allow/deny 결과를 어떻게 remediation 친화적인 finding 구조로 다시 잘랐는지, 그리고 safe policy 0건까지 어떻게 품질 기준으로 삼았는지 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 왜 "허용됐다"는 사실만으로는 운영 triage가 되지 않았는가
- broad admin과 passrole을 왜 서로 다른 control 조합으로 나눠야 했는가
- 이 analyzer가 지금 무엇을 잡고, 무엇은 아직 의도적으로 놓치고 있는가

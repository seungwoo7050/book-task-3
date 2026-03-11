# 문제 정리

## 원래 문제

IAM policy JSON을 읽고, 단순 allow/deny가 아니라 least privilege 관점에서 설명 가능한 finding을 만들어야 합니다.
정책이 왜 위험한지와 어떤 패턴이 remediation 우선순위를 높이는지 함께 드러나야 합니다.

## 제공된 자료

- `problem/data/broad_admin_policy.json`
- `problem/data/passrole_policy.json`
- `problem/data/scoped_policy.json`

## 제약

- 조직 전체 권한 그래프는 추적하지 않습니다.
- policy analyzer는 단일 policy 문서 기준의 위험 판단까지만 담당합니다.

## 통과 기준

- broad admin 정책에서 고위험 finding이 나와야 합니다.
- `iam:PassRole`이 escalation finding으로 분리되어야 합니다.
- safe policy에서 0건이 나오는 테스트가 유지되어야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- SCP
- permission boundary
- condition 기반 privilege narrowing

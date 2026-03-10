# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

정책이 허용되는지만으로는 보안 운영에 충분하지 않습니다. 이 프로젝트는 IAM policy를 읽고, least privilege 관점에서
바로 triage 가능한 finding을 만드는 것이 목표입니다. 즉, 질문이 `allowed?`에서 `how risky?`로 바뀝니다.

## 실제 입력과 출력

입력:
- `broad_admin_policy.json`
- `passrole_policy.json`
- `scoped_policy.json`

출력:
- control_id가 붙은 finding 목록
- severity와 사람이 읽을 수 있는 title
- evidence_ref 같은 후속 처리를 위한 필드

## 강한 제약

- SCP, permission boundary, condition-based narrowing은 다루지 않습니다.
- 조직 전체 권한 그래프나 cross-account trust 분석은 범위 밖입니다.
- 그러나 finding 데이터 구조는 이후 프로젝트와 공유될 정도로 명확해야 합니다.

## 완료로 보는 기준

- broad admin 정책에서 여러 finding이 동시에 나와야 합니다.
- `iam:PassRole` 같은 escalation action이 별도 규칙으로 잡혀야 합니다.
- scoped read-only 정책은 finding 0개로 통과해야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_analyzer.py](../python/tests/test_analyzer.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)

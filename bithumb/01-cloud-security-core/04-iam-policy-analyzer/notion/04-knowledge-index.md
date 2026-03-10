# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- `Finding`은 정적 분석 결과를 사람이 읽고 시스템이 재사용할 수 있는 공통 레코드입니다.
- broadness와 escalation은 서로 다른 위험 축이므로, 같은 action set 안에 있어도 별도 control로 관리할 수 있습니다.
- negative test는 analyzer 품질의 핵심 증거입니다.
- finding 구조가 안정적이어야 remediation, exception, report까지 연결됩니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/least-privilege-findings.md](../docs/concepts/least-privilege-findings.md)
- 구현 진입점: [../python/src/iam_policy_analyzer/analyzer.py](../python/src/iam_policy_analyzer/analyzer.py)
- CLI 진입점: [../python/src/iam_policy_analyzer/cli.py](../python/src/iam_policy_analyzer/cli.py)
- 검증 코드: [../python/tests/test_analyzer.py](../python/tests/test_analyzer.py)
- 입력 fixture: [../problem/data/](../problem/data/)

## 재현 체크포인트

- `broad_admin_policy.json`을 넣었을 때 `IAM-001`, `IAM-002` 두 control이 모두 나오는지 확인합니다.
- `passrole_policy.json`은 `IAM-003` escalation finding을 따로 만들 수 있어야 합니다.
- `scoped_policy.json`은 빈 리스트를 반환해야 analyzer가 과도하게 시끄럽지 않다는 뜻입니다.

## 다음 프로젝트로 이어지는 질문

- `05-cspm-rule-engine`은 같은 finding 구조를 Terraform misconfiguration으로 옮깁니다.
- `06-remediation-pack-runner`는 finding을 dry-run remediation plan으로 바꿉니다.
- `10-cloud-security-control-plane`은 이 analyzer 결과를 API와 DB 흐름으로 통합합니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)

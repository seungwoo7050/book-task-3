# 문서 묶음 안내

이 문서 묶음은 capstone을 "보안 기능 모음"이 아니라 "한 서비스 review를 설명하는 최소 운영 문서"로 읽게 만드는 안내서입니다.

## 먼저 보면 좋은 질문

- 왜 `security-core` capstone은 API 서버가 아니라 offline review pipeline인가
- foundations에서 분리했던 control vocabulary를 remediation board 한 장으로 어떻게 다시 정렬하는가
- 어떤 항목은 즉시 수정하고 어떤 항목은 queue로 남기는가

## 읽고 나면 설명할 수 있어야 하는 것

- `crypto_review`, `auth_scenarios`, `backend_cases`, `dependency_bundle`을 왜 따로 입력으로 둔 이유
- `high -> P1`, `medium -> P2`, `low -> P3` 정규화 규칙과 dependency priority 유지 이유
- `.artifacts/capstone/demo/`의 7개 산출물이 각각 어떤 독자를 위한 것인지

## 함께 보면 좋은 문서

1. [concepts/consolidated-remediation-workflow.md](concepts/consolidated-remediation-workflow.md)
2. [demo-walkthrough.md](demo-walkthrough.md)
3. [references/README.md](references/README.md)
4. [../problem/README.md](../problem/README.md)

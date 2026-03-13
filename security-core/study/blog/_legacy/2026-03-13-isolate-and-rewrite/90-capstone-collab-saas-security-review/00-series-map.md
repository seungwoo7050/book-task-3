# collab-saas-security-review series map

이 시리즈는 `collab-saas-security-review`를 "보안 기능 모음"이 아니라, crypto, auth, backend, dependency 판단을 하나의 remediation board와 artifact 세트로 다시 묶는 offline review pipeline으로 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- foundations 프로젝트에서 분리해 둔 control vocabulary를 그대로 유지하면서도, 하나의 서비스 review로 다시 엮으려면 어떤 조합 규칙이 필요할까
- category별 finding과 dependency priority를 한 우선순위 언어로 다시 정렬하면 무엇이 먼저 고쳐져야 하는지가 어떻게 보일까

## 읽는 순서

1. [10-chronology-reusing-foundation-vocabulary-in-one-review.md](10-chronology-reusing-foundation-vocabulary-in-one-review.md)
2. [20-chronology-remediation-board-and-artifact-report.md](20-chronology-remediation-board-and-artifact-report.md)

## 참조한 실제 파일

- `study/90-capstone-collab-saas-security-review/README.md`
- `study/90-capstone-collab-saas-security-review/problem/README.md`
- `study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json`
- `study/90-capstone-collab-saas-security-review/problem/data/secure_baseline_bundle.json`
- `study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json`
- `study/90-capstone-collab-saas-security-review/docs/concepts/consolidated-remediation-workflow.md`
- `study/90-capstone-collab-saas-security-review/docs/demo-walkthrough.md`
- `study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py`
- `study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py`
- `study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py`
- `study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/dependency.py`
- `study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/review.py`
- `study/90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py`
- `study/90-capstone-collab-saas-security-review/python/tests/test_review.py`
- `study/90-capstone-collab-saas-security-review/python/tests/test_cli.py`

## Canonical CLI

```bash
cd study/90-capstone-collab-saas-security-review
PYTHONPATH=python/src ../../.venv/bin/python -m pytest python/tests
PYTHONPATH=python/src ../../.venv/bin/python -m collab_saas_security_review.cli review problem/data/review_bundle.json
PYTHONPATH=python/src ../../.venv/bin/python -m collab_saas_security_review.cli demo problem/data/demo_bundle.json
```

## Git Anchor

- `2026-03-12 e3be503 Track Appendix 에 대한 전반적인 개선 완료 (mobile / security)`

## 추론 원칙

- chronology는 `consolidated-remediation-workflow.md`가 먼저 고정한 category 구조와 `review.py`의 조합 규칙을 따라 복원했다.
- 이 capstone의 끝은 finding count를 요약하는 데 있지 않고, review JSON, remediation board, artifact 7종이 같은 vocabulary로 일관되게 닫히는 지점으로 본다.

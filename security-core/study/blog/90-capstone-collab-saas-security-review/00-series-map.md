# Series Map — collab-saas-security-review

이 시리즈는 앞선 네 프로젝트에서 만든 vocabulary를 마지막에 어떻게 한 서비스 review로 다시 묶는지 따라간다. 읽는 순서도 통합용 surface에 맞춰 잡혀 있다. 먼저 category evaluator를 다시 세우고, 그 결과를 remediation board로 정렬한 뒤, 마지막에 artifact와 report가 실제로 어떻게 만들어지는지 확인한다.

## 범위

- 핵심 질문: crypto, auth, backend, dependency에서 나온 서로 다른 판단을 하나의 remediation board와 artifact 세트로 어떻게 다시 묶을 것인가.
- 글의 단위: category별 evaluator 재구성 -> consolidated review 조합 -> artifact/report 출력.
- chronology 표지: 세부 commit이 없어서 `Session 1`부터 `Session 4`까지로 복원한다.

## source set

문제 정의와 개념 문서는 “왜 offline review pipeline인가”를 설명하고, `review.py`와 CLI 테스트는 실제 정렬 규칙과 artifact contract를 고정한다.

- `../../90-capstone-collab-saas-security-review/README.md`
- `../../90-capstone-collab-saas-security-review/problem/README.md`
- `../../90-capstone-collab-saas-security-review/docs/README.md`
- `../../90-capstone-collab-saas-security-review/docs/concepts/consolidated-remediation-workflow.md`
- `../../90-capstone-collab-saas-security-review/docs/demo-walkthrough.md`
- `../../90-capstone-collab-saas-security-review/python/README.md`
- `../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py`
- `../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py`
- `../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py`
- `../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/dependency.py`
- `../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/review.py`
- `../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py`
- `../../90-capstone-collab-saas-security-review/python/tests/test_review.py`
- `../../90-capstone-collab-saas-security-review/python/tests/test_cli.py`

## canonical CLI

```bash
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m pytest study/90-capstone-collab-saas-security-review/python/tests

PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json

PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli demo \
  study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-chronology-reassembling-findings-into-one-remediation-board.md](10-chronology-reassembling-findings-into-one-remediation-board.md)

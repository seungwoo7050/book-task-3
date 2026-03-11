# python

이 프로젝트의 Python 구현은 입력 bundle을 읽어 consolidated review와 artifact를 생성하는 CLI 패키지입니다.

## 주요 명령

```bash
PYTHONPATH=study/Capstone/collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/Capstone/collab-saas-security-review/problem/data/review_bundle.json

PYTHONPATH=study/Capstone/collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli demo \
  study/Capstone/collab-saas-security-review/problem/data/demo_bundle.json
```

## 테스트

```bash
make test-capstone
```

## 구현 메모

- `crypto.py`, `auth.py`, `backend.py`, `dependency.py`는 각 카테고리의 evaluator를 분리합니다.
- `review.py`는 consolidated review, remediation board, artifact report를 생성합니다.
- `cli.py`는 `review`, `demo`만 공개합니다.

# Python 구현

## 구현 개요

이 구현은 review bundle을 읽어 consolidated review JSON, remediation board, markdown report, artifact 세트를 생성하는 Python 패키지입니다.

## 핵심 모듈

- `src/collab_saas_security_review/crypto.py`: crypto review evaluator
- `src/collab_saas_security_review/auth.py`: auth scenario evaluator
- `src/collab_saas_security_review/backend.py`: backend case evaluator
- `src/collab_saas_security_review/dependency.py`: dependency triage 재구성
- `src/collab_saas_security_review/review.py`: review 결합, remediation board 정렬, report/artifact 생성
- `src/collab_saas_security_review/cli.py`: `review`, `demo` 명령 공개

## CLI 계약

```bash
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json

PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli demo \
  study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json
```

- `review <bundle>`: consolidated review JSON을 출력합니다.
- `demo <bundle>`: artifact 세트를 생성하고 생성 위치를 출력합니다.

## 테스트

```bash
make test-capstone
```

카테고리별 evaluator는 분리하고, review 조합과 artifact 생성은 `review.py`에서만 담당하게 구성했습니다.

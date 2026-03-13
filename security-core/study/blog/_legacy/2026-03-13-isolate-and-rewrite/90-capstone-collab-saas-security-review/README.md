# collab-saas-security-review blog

이 디렉터리는 `collab-saas-security-review`를 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 README, review bundle, 개념 문서, capstone Python 구현, pytest, 실제 review/demo CLI 출력만으로 복원했다.

## source set

- [../../90-capstone-collab-saas-security-review/README.md](../../90-capstone-collab-saas-security-review/README.md)
- [../../90-capstone-collab-saas-security-review/problem/README.md](../../90-capstone-collab-saas-security-review/problem/README.md)
- [../../90-capstone-collab-saas-security-review/problem/data/review_bundle.json](../../90-capstone-collab-saas-security-review/problem/data/review_bundle.json)
- [../../90-capstone-collab-saas-security-review/problem/data/secure_baseline_bundle.json](../../90-capstone-collab-saas-security-review/problem/data/secure_baseline_bundle.json)
- [../../90-capstone-collab-saas-security-review/problem/data/demo_bundle.json](../../90-capstone-collab-saas-security-review/problem/data/demo_bundle.json)
- [../../90-capstone-collab-saas-security-review/docs/README.md](../../90-capstone-collab-saas-security-review/docs/README.md)
- [../../90-capstone-collab-saas-security-review/docs/concepts/consolidated-remediation-workflow.md](../../90-capstone-collab-saas-security-review/docs/concepts/consolidated-remediation-workflow.md)
- [../../90-capstone-collab-saas-security-review/docs/demo-walkthrough.md](../../90-capstone-collab-saas-security-review/docs/demo-walkthrough.md)
- [../../90-capstone-collab-saas-security-review/python/README.md](../../90-capstone-collab-saas-security-review/python/README.md)
- [../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py](../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/crypto.py)
- [../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py](../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/auth.py)
- [../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py](../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/backend.py)
- [../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/dependency.py](../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/dependency.py)
- [../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/review.py](../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/review.py)
- [../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py](../../90-capstone-collab-saas-security-review/python/src/collab_saas_security_review/cli.py)
- [../../90-capstone-collab-saas-security-review/python/tests/test_review.py](../../90-capstone-collab-saas-security-review/python/tests/test_review.py)
- [../../90-capstone-collab-saas-security-review/python/tests/test_cli.py](../../90-capstone-collab-saas-security-review/python/tests/test_cli.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-reusing-foundation-vocabulary-in-one-review.md](10-chronology-reusing-foundation-vocabulary-in-one-review.md)
3. [20-chronology-remediation-board-and-artifact-report.md](20-chronology-remediation-board-and-artifact-report.md)
4. [../../90-capstone-collab-saas-security-review/README.md](../../90-capstone-collab-saas-security-review/README.md)

## 검증 진입점

```bash
cd ../../..
make venv
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m pytest study/90-capstone-collab-saas-security-review/python/tests
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli review \
  study/90-capstone-collab-saas-security-review/problem/data/review_bundle.json
PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src \
  .venv/bin/python -m collab_saas_security_review.cli demo \
  study/90-capstone-collab-saas-security-review/problem/data/demo_bundle.json
```

## chronology 메모

- chronology는 `foundation vocabulary 재구성 -> consolidated review 조합 -> remediation board 정렬 -> artifact/report 출력` 순으로 복원했다.
- 핵심 전환점은 앞선 프로젝트를 import하지 않으면서도 같은 control ID와 priority vocabulary를 유지하게 만든 지점이다.

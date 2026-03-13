# owasp-backend-mitigations blog

이 디렉터리는 `owasp-backend-mitigations`를 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 README, case fixture, 개념 문서, evaluator, pytest, 실제 CLI 출력만으로 복원했다.

## source set

- [../../03-owasp-backend-mitigations/README.md](../../03-owasp-backend-mitigations/README.md)
- [../../03-owasp-backend-mitigations/problem/README.md](../../03-owasp-backend-mitigations/problem/README.md)
- [../../03-owasp-backend-mitigations/problem/data/case_bundle.json](../../03-owasp-backend-mitigations/problem/data/case_bundle.json)
- [../../03-owasp-backend-mitigations/problem/data/demo_profile.json](../../03-owasp-backend-mitigations/problem/data/demo_profile.json)
- [../../03-owasp-backend-mitigations/docs/README.md](../../03-owasp-backend-mitigations/docs/README.md)
- [../../03-owasp-backend-mitigations/docs/concepts/backend-defense-five.md](../../03-owasp-backend-mitigations/docs/concepts/backend-defense-five.md)
- [../../03-owasp-backend-mitigations/python/README.md](../../03-owasp-backend-mitigations/python/README.md)
- [../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py](../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py)
- [../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cases.py](../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cases.py)
- [../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cli.py](../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cli.py)
- [../../03-owasp-backend-mitigations/python/tests/test_evaluator.py](../../03-owasp-backend-mitigations/python/tests/test_evaluator.py)
- [../../03-owasp-backend-mitigations/python/tests/test_cli.py](../../03-owasp-backend-mitigations/python/tests/test_cli.py)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-route-surfaces-case-matrix-and-demo-gateway.md](10-chronology-route-surfaces-case-matrix-and-demo-gateway.md)
3. [../../03-owasp-backend-mitigations/README.md](../../03-owasp-backend-mitigations/README.md)

## 검증 진입점

```bash
cd ../../..
make venv
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m pytest study/03-owasp-backend-mitigations/python/tests
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/03-owasp-backend-mitigations/problem/data/case_bundle.json
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli demo \
  study/03-owasp-backend-mitigations/problem/data/demo_profile.json
```

## chronology 메모

- chronology는 `backend defense five vocabulary -> case matrix -> all-gaps demo route` 순으로 복원했다.
- 핵심 전환점은 OWASP 이름을 외우는 단계에서 멈추지 않고, route surface와 control 누락을 같은 fixture에 같이 적는 방식으로 바꾼 지점이다.

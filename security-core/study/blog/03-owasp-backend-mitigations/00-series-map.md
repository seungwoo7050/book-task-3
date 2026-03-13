# Series Map — owasp-backend-mitigations

이 시리즈는 backend 보안을 OWASP 항목 이름 요약으로 끝내지 않고, route surface에서 빠진 방어를 finding으로 바꾸는 흐름을 따라간다. 읽는 순서도 route 중심이다. 먼저 defense vocabulary를 세우고, 그 다음 case bundle로 negative case를 고정한 뒤, 마지막에 composite demo로 여러 방어 경계가 한 endpoint에 겹치는 장면까지 보여 준다.

## 범위

- 핵심 질문: backend route에서 반복되는 방어 경계를 어떻게 fixture와 finding으로 고정할 것인가.
- 글의 단위: route defense vocabulary 정의 -> case bundle summary -> demo/CLI 계약.
- chronology 표지: 세부 commit이 없어서 `Session 1`부터 `Session 3`까지로 복원한다.

## source set

README와 개념 문서는 “어떤 route surface를 볼 것인가”를 정하고, `evaluator.py`, `cases.py`, CLI 테스트가 그 질문을 반복 가능한 계약으로 바꾼다.

- `../../03-owasp-backend-mitigations/README.md`
- `../../03-owasp-backend-mitigations/problem/README.md`
- `../../03-owasp-backend-mitigations/docs/README.md`
- `../../03-owasp-backend-mitigations/docs/concepts/backend-defense-five.md`
- `../../03-owasp-backend-mitigations/python/README.md`
- `../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py`
- `../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cases.py`
- `../../03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cli.py`
- `../../03-owasp-backend-mitigations/python/tests/test_evaluator.py`
- `../../03-owasp-backend-mitigations/python/tests/test_cli.py`

## canonical CLI

```bash
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m pytest study/03-owasp-backend-mitigations/python/tests

PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/03-owasp-backend-mitigations/problem/data/case_bundle.json

PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli demo \
  study/03-owasp-backend-mitigations/problem/data/demo_profile.json
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-chronology-fixing-route-defense-gaps-with-case-fixtures.md](10-chronology-fixing-route-defense-gaps-with-case-fixtures.md)

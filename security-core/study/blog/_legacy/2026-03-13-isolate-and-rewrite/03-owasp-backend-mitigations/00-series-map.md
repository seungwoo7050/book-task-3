# owasp-backend-mitigations series map

이 시리즈는 `owasp-backend-mitigations`를 "취약점 이름 모음"이 아니라, route surface에서 어떤 방어 경계가 빠졌는지를 fixture로 재현하는 lab으로 다시 읽기 위한 지도다.

## 이 프로젝트가 답하는 질문

- backend 보안을 framework나 ORM 기능 소개가 아니라 route-level control gap으로 설명하려면 어떤 vocabulary가 필요할까
- secure baseline과 negative case를 같은 bundle에 두면 OWASP 이야기가 왜 훨씬 덜 추상적으로 읽힐까

## 읽는 순서

1. [10-chronology-route-surfaces-case-matrix-and-demo-gateway.md](10-chronology-route-surfaces-case-matrix-and-demo-gateway.md)

## 참조한 실제 파일

- `study/03-owasp-backend-mitigations/README.md`
- `study/03-owasp-backend-mitigations/problem/README.md`
- `study/03-owasp-backend-mitigations/problem/data/case_bundle.json`
- `study/03-owasp-backend-mitigations/problem/data/demo_profile.json`
- `study/03-owasp-backend-mitigations/docs/concepts/backend-defense-five.md`
- `study/03-owasp-backend-mitigations/python/README.md`
- `study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/evaluator.py`
- `study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cases.py`
- `study/03-owasp-backend-mitigations/python/src/owasp_backend_mitigations/cli.py`
- `study/03-owasp-backend-mitigations/python/tests/test_evaluator.py`
- `study/03-owasp-backend-mitigations/python/tests/test_cli.py`

## Canonical CLI

```bash
cd study/03-owasp-backend-mitigations
PYTHONPATH=python/src ../../.venv/bin/python -m pytest python/tests
PYTHONPATH=python/src ../../.venv/bin/python -m owasp_backend_mitigations.cli check-cases problem/data/case_bundle.json
PYTHONPATH=python/src ../../.venv/bin/python -m owasp_backend_mitigations.cli demo problem/data/demo_profile.json
```

## Git Anchor

- `2026-03-12 e3be503 Track Appendix 에 대한 전반적인 개선 완료 (mobile / security)`

## 추론 원칙

- chronology는 `backend-defense-five.md`가 먼저 고정한 다섯 질문과 evaluator의 분기 조건을 따라 복원했다.
- 이 lab의 끝은 route 하나를 설명하는 데 있지 않고, bundle 전체가 `passed: 6`, `failed: 0`으로 닫히면서 secure baseline과 negative case가 같이 살아남는 지점으로 본다.

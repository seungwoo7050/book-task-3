# owasp-backend-mitigations

## 프로젝트 한줄 소개

대표적인 backend defense control 누락을 endpoint fixture에서 바로 찾는 OWASP mitigation evaluator입니다.

## 왜 배우는가

OWASP Top 10 전체를 한 번에 외우는 것보다, 실제 backend에서 반복적으로 설명해야 하는 입력/출력 경계 몇 개를 먼저 분리하는 편이 더 실용적입니다.
이 프로젝트는 injection, broken access control, SSRF, debug exposure, path traversal을 작은 route fixture로 평가합니다.

## 현재 구현 범위

- endpoint case manifest 평가
- `OWASP-001`~`OWASP-005` finding 반환
- `check-cases`와 `demo` CLI
- secure baseline 0 finding 검증

## 빠른 시작

```bash
make venv
make demo-owasp
PYTHONPATH=study/Foundations-Security/owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/Foundations-Security/owasp-backend-mitigations/problem/data/case_bundle.json
```

## 검증 명령

```bash
make test-unit
```

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)
- [guides/security/owasp-backend-defense.md](../../../../guides/security/owasp-backend-defense.md)

## 포트폴리오 확장 힌트

취약점 이름을 나열하는 것보다 어떤 입력 경계에서 어떤 방어를 요구하는지와, secure baseline이 왜 0 finding인지 설명하는 편이 좋습니다.

## 알려진 한계

- 실제 FastAPI/Spring app, DB, outbound network는 구현하지 않습니다.
- XSS, deserialization, authz-as-code 같은 다른 OWASP 주제는 현재 범위 밖입니다.


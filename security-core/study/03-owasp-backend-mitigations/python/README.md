# Python 구현

## 구현 개요

이 구현은 endpoint case fixture를 읽어 defense gap을 `OWASP-*` finding으로 바꾸는 Python evaluator 패키지입니다.

## 핵심 모듈

- `src/owasp_backend_mitigations/evaluator.py`: control meta와 case 판정 로직
- `src/owasp_backend_mitigations/cases.py`: manifest 로딩, summary 계산, demo profile 변환
- `src/owasp_backend_mitigations/cli.py`: `check-cases`, `demo` 명령 공개

## CLI 계약

```bash
PYTHONPATH=study/03-owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/03-owasp-backend-mitigations/problem/data/case_bundle.json
```

- `check-cases <manifest>`: `passed`, `failed`, `cases`를 JSON으로 출력합니다.
- `demo <profile>`: `control_ids`와 `findings`를 JSON으로 출력합니다.

## 테스트

```bash
make test-unit
```

실제 framework 없이도 route defense와 evidence를 설명할 수 있게 `attack`, `mitigation`, `evidence`를 함께 반환합니다.

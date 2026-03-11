# Python 구현

## 다루는 범위

- endpoint case fixture 읽기
- mitigation 누락을 `OWASP-001`~`OWASP-005` finding으로 변환
- `check-cases` summary 출력
- `demo` single-profile 출력

## 실행 예시

```bash
make venv
PYTHONPATH=study/Foundations-Security/owasp-backend-mitigations/python/src \
  .venv/bin/python -m owasp_backend_mitigations.cli check-cases \
  study/Foundations-Security/owasp-backend-mitigations/problem/data/case_bundle.json
```

## 테스트

```bash
make test-unit
```

## 상태

`verified`

## 구현 메모

이 프로젝트는 실제 app framework 없이도 route defense가 어디서 필요한지 설명하는 데 집중합니다. finding은 attack, mitigation, evidence를 함께 반환합니다.


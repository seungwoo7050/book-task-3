# 08-capstone-submission 디버그 기록

## 검증 메모

- `v0`, `v1`, `v2` 모두 `UV_PYTHON=python3.12 make gate-all`을 통과시켰다.
- `v1`, `v2`에서 `make smoke-postgres`를 통과시켰다.
- baseline/candidate compare 결과는 `avg_score 84.06 -> 87.76`, `critical 2 -> 0`, `pass 16 -> 19`, `fail 14 -> 11`이다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: `make gate-all`이 기본 Python 3.14 환경에서 `chromadb` import 문제로 깨졌다.
- 원인: 실사용 dependency 조합이 Python 3.12를 전제로 안정화되어 있었기 때문이다.
- 수정: 각 Python 구현에 `.python-version`과 `requires-python >=3.12,<3.13` 계약을 추가하고 검증 명령도 `UV_PYTHON=python3.12`로 고정했다.
- 확인: v0, v1, v2 모두 `UV_PYTHON=python3.12 make gate-all`을 통과했다.

### 사례 2
- 증상: baseline 실패 원인 중 `MISSING_REQUIRED_EVIDENCE_DOC` 비중이 높았다.
- 원인: retrieval이 도메인/리스크 힌트를 충분히 사용하지 못해 답변이 필요한 문서를 놓쳤다.
- 수정: v2에 alias, category hint, risk-aware doc preference, retrieval-conditioned answer composer를 추가했다.
- 확인: v2 compare 결과에서 fail count가 14에서 11로 줄고 critical count가 2에서 0으로 감소했다.

## 재발 방지 체크리스트

- `08-capstone-submission/README.md`
- `08-capstone-submission/docs/release-readiness.md`
- `08-capstone-submission/v0-initial-demo`
- `08-capstone-submission/v1-regression-hardening`
- `08-capstone-submission/v2-submission-polish`

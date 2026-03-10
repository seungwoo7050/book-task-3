# 01-quality-rubric-and-score-contract 디버그 기록

## 검증 메모

- 테스트는 weight sum, critical override, high-score grade band를 검증한다.
- 이 단계는 LLM judge 품질이 아니라 merge contract 안정성을 검증한다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: critical failure가 있어도 평균 점수가 높게 계산될 수 있었다.
- 원인: weighted average만 사용하면 severe compliance 위반이 다른 축에 묻힐 수 있다.
- 수정: `critical=True`일 때 즉시 `CRITICAL` 결과를 반환하도록 분기했다.
- 확인: `test_critical_override_wins`가 100점 입력에서도 `CRITICAL`을 기대한다.

## 재발 방지 체크리스트

- `python/src/stage01/rubric.py`
- `python/tests/test_rubric.py`

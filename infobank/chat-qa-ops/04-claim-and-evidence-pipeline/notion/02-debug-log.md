# 04-claim-and-evidence-pipeline 디버그 기록

## 검증 메모

- 테스트는 첫 claim이 `support` verdict와 예상 doc trace를 남기는지 확인한다.
- silent success보다 trace completeness를 더 중요하게 본다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: 근거가 없는 claim이 결과 구조에서 사라지면 왜 groundedness가 낮은지 설명하기 어려웠다.
- 원인: matched docs가 없는 claim을 trace 없이 버리면 failure 분석이 불가능하다.
- 수정: `not_found` verdict와 빈 docs list를 포함한 claim result를 항상 반환하도록 했다.
- 확인: 테스트와 구현에서 모든 claim이 결과 리스트에 유지된다.

## 재발 방지 체크리스트

- `python/src/stage04/pipeline.py`
- `python/tests/test_pipeline.py`

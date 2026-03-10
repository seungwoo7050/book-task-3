# 06-golden-set-and-regression 디버그 기록

## 검증 메모

- 테스트는 golden assertion success와 manifest labels를 함께 검증한다.
- stage 범위는 데이터셋 계약까지이며 dashboard 저장소는 포함하지 않는다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: baseline과 candidate가 어떤 run label인지 문서만 봐서는 혼동될 수 있었다.
- 원인: compare input이 코드 호출부에만 숨어 있으면 proof artifact와 추적이 끊긴다.
- 수정: `compare_manifest.json`에 baseline, candidate, dataset을 분리 저장했다.
- 확인: `test_golden_assertion_and_compare_manifest`가 `v1.0`, `v1.1`, `golden-set` 값을 검증한다.

## 재발 방지 체크리스트

- `python/data/golden_cases.json`
- `python/data/compare_manifest.json`
- `python/src/stage06/regression.py`

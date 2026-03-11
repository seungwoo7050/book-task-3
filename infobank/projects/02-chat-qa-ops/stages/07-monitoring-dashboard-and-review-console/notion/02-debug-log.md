# 07-monitoring-dashboard-and-review-console 디버그 기록

## 검증 메모

- Python pack은 snapshot endpoint contract를 테스트한다.
- React pack은 mocked Vitest로 overview, failures, session review, eval runner, compare UI를 검증한다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: 문서 생성이 너무 얇으면 stage07이 단순 UI 복사본처럼 보였다.
- 원인: overview, failures, session review, compare가 각각 어떤 운영 질문에 답하는지 서술이 없었다.
- 수정: problem/docs/notion에 화면별 책임과 trace surface를 명시적으로 추가했다.
- 확인: 재생성된 stage07 문서가 API/React pack과 version compare 목적을 구분해 설명한다.

## 재발 방지 체크리스트

- `python/src/stage07/app.py`
- `python/tests/test_api.py`
- `react/src/pages/Overview.tsx`
- `react/src/pages/SessionReview.tsx`

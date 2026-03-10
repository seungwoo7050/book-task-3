# 05-judge-and-score-merge 디버그 기록

## 검증 메모

- 테스트는 failure가 없는 응답의 total score와 empty failure types를 검증한다.
- 이 stage는 live provider 품질보다 interface boundary를 보는 것이 목적이다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: 짧은 응답도 무조건 높은 resolution 점수를 받을 수 있었다.
- 원인: 응답 길이와 안내성 표현을 별도 기준으로 보지 않으면 resolution과 communication이 구분되지 않는다.
- 수정: response length와 안내/확인 표현 유무로 resolution, communication을 분리했다.
- 확인: `judge_response` 구현이 길이와 표현 여부를 다른 축으로 평가한다.

## 재발 방지 체크리스트

- `python/src/stage05/judge.py`
- `python/tests/test_judge.py`

# 05 judge 결과와 점수 병합 문제 정의

judge 결과와 rubric merge를 분리해 품질 판단과 점수 계산의 경계를 명확히 만드는 단계다.

## 문제 해석

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?

## 입력

- user message
- assistant response
- failure types
- groundedness와 compliance 서브스코어

## 기대 산출물

- judge result dictionary
- weighted final score

## 완료 기준

- judge와 scorer가 별도 함수 계약을 가진다.
- failure types는 판단 결과와 최종 score 계산 모두에 반영된다.
- live provider가 없어도 deterministic 테스트가 가능하다.

## 현재 확인 가능한 증거

- `python/tests/test_judge.py`가 judge+merge 조합 결과를 검증한다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: heuristic judge, score merge contract
- 이번 단계에서 일부러 제외한 범위: LLM adapter 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`

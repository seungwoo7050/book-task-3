# 05-judge-and-score-merge 문제 정의

## 이 stage가 푸는 문제

judge 결과와 rubric merge를 분리해 품질 판단과 점수 계산의 경계를 명확히 만드는 단계다.

## 성공 기준

- judge와 scorer가 별도 함수 계약을 가진다.
- failure types는 판단 결과와 최종 score 계산 모두에 반영된다.
- live provider가 없어도 deterministic 테스트가 가능하다.

## 왜 지금 이 단계를 먼저 보는가

- v1의 LLM judge trace와 stage01 rubric contract 사이를 잇는 중간 단계다.
- 추후 provider가 바뀌어도 merge contract는 유지된다는 점을 보여준다.

## 먼저 알고 있으면 좋은 것

- stage01의 weighted rubric과 stage03의 failure taxonomy를 알고 있어야 한다.

## 확인할 증거

- `python/tests/test_judge.py`가 judge+merge 조합 결과를 검증한다.

## 아직 남아 있는 불확실성

heuristic judge는 실제 상담 품질의 뉘앙스를 충분히 반영하지 못한다. stage 목적은 interface freeze다.

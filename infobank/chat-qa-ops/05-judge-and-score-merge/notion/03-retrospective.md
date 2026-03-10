# 05-judge-and-score-merge 회고

## 이번 stage로 강화된 점

- judge 모델을 바꾸어도 merge 검증은 그대로 유지된다.
- failure taxonomy와 score axes의 연결이 명확하다.

## 아직 약한 부분

- heuristic 기준이 실제 상담 품질 평가자 합의와 일치한다고 보장할 수 없다.

## 학생이 여기서 바로 가져갈 것

- judge 모델 출력과 최종 점수 산식을 분리해, 모델 교체와 품질 계약을 따로 관리하는 방식
- score axes, hard fail, explanation text를 한 객체에 과도하게 섞지 않고 경계를 두는 방식

## 다음 stage로 넘기는 자산

- judge output schema
- heuristic scoring
- quality axes merge

## 05-development-timeline.md와 같이 읽을 포인트

- judge schema 테스트와 score merge 테스트를 따로 확인해 어떤 계약이 어디서 보장되는지 나눠 본다.
- 이후 regression stage를 읽을 때는 compare 대상이 judge 출력 변화인지 merge 규칙 변화인지 구분해서 본다.

## 나중에 다시 볼 것

- 향후 live judge 출력과 heuristic judge 출력을 같은 schema로 비교하는 회귀 실험을 추가할 수 있다.

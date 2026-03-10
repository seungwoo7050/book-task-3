# Judge & Score Merge — 회고

## 잘 된 것

### judge 모델을 바꿔도 merge 검증은 그대로 유지

이게 이 stage의 가장 큰 성과다.
v1에서 LLM judge로 교체했을 때, merge_score() 함수와 그 테스트는 **한 줄도 바꾸지 않았다**.
judge output의 schema만 같으면 merge는 신경 쓸 필요가 없다.

### failure taxonomy와 score axes의 연결이 명확하다

failure_types(stage 03 출력) → correctness 감점(judge) → total score(merge) → grade(rubric)
이 흐름이 코드 수준에서 추적 가능하다.

## 아쉬운 것

### heuristic 기준이 실제 상담 품질 평가자 합의와 일치한다고 보장할 수 없다

response 길이가 10자 넘으면 resolution 85점이라는 건, 실제 상담 전문가가 동의할 결과가 아니다.
하지만 이 stage의 목적이 judge 정교화가 아니라 **interface freeze**이므로, 의도적인 타협이다.

## 나중에 다시 볼 것

- live judge 출력과 heuristic judge 출력을 같은 schema로 비교하는 회귀 실험을 추가하면, heuristic이 얼마나 벗어나는지 수치화할 수 있다.

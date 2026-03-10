# Quality Rubric — 회고: 점수 체계를 고정한 뒤

## 잘 된 것

### 후속 stage에서 judge와 evidence verifier를 독립 개발할 수 있게 됐다

stage 03(guardrail), stage 04(evidence pipeline), stage 05(judge)를 만들 때, 각각의 출력이 최종 점수에 어떻게 합산되는지 미리 알고 있었다.
"compliance 위반은 critical을 트리거한다", "groundedness는 25% weight다"라는 규칙이 코드로 고정되어 있으니, 각 stage의 개발자가 자기 영역만 집중하면 됐다.

### 평가 결과를 비교할 때 score drift 원인을 좁히기 쉬워졌다

v0과 v1의 점수가 다를 때, "rubric이 바뀌었나?"는 확인하지 않아도 된다. rubric은 얼어 있으니까.
점수 변동의 원인은 judge이거나, input data이거나, retrieval이다. 원인 탐색 범위가 줄었다.

## 아쉬운 것

### grade band 임계값은 아직 empirical tuning이 아니다

A≥90, B≥75, C≥60, D≥40이라는 기준은 직관적이긴 하지만, 실제 상담 데이터를 수십 건 평가한 뒤 조정한 값이 아니다.
"B 등급인데 실제로는 꽤 안 좋은 답변"이 나올 수 있다.
하지만 이 단계의 목적이 calibration이 아니라 contract freeze였기 때문에, 이건 의도적인 타협이다.

## 나중에 다시 볼 것

- 실제 golden set 평가를 더 모으면, threshold calibration 근거를 추가할 수 있다.
- grade band를 단순 고정값이 아니라 설정 가능한 구조로 바꾸는 것도 고려할 수 있지만, 지금은 단순함이 더 중요하다.

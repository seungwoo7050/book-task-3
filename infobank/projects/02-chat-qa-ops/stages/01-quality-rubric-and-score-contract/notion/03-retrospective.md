# 01-quality-rubric-and-score-contract 회고

## 이번 stage로 강화된 점

- 후속 stage에서 judge와 evidence verifier를 독립 개발할 수 있다.
- 평가 결과를 비교할 때 score drift 원인을 좁히기 쉽다.

## 아직 약한 부분

- grade band 임계값은 아직 empirical tuning이 아니다.

## 학생이 여기서 바로 가져갈 것

- 점수 축과 hard fail을 같은 표에 섞지 않고 별도 계약으로 분리하는 방식
- judge 모델이 바뀌어도 score merge 규칙은 흔들리지 않게 문서화하는 방식

## 다음 stage로 넘기는 자산

- weighted rubric 설계
- critical override와 grade band의 분리
- judge 출력과 final score merge 계약

## 05-development-timeline.md와 같이 읽을 포인트

- 테스트 명령을 따라가며 어떤 임계값이 코드에 고정돼 있는지 먼저 확인한다.
- 이후 stage에서 judge나 evidence verifier를 읽을 때 이 rubric contract를 기준면으로 다시 대조한다.

## 나중에 다시 볼 것

- 실제 golden set 평가를 더 모으면 threshold calibration 근거를 추가할 수 있다.

# 06-golden-set-and-regression 회고

## 이번 stage로 강화된 점

- 비교 대상과 데이터셋 범위가 명시적이다.
- failure type 감소를 개선의 근거로 삼기 쉽다.

## 아직 약한 부분

- 실제 capstone처럼 run registry나 dashboard와 연결되지는 않는다.

## 학생이 여기서 바로 가져갈 것

- compare와 regression을 말로 설명하지 않고 dataset, manifest, assertion으로 고정하는 방식
- failure type 감소를 개선 근거로 삼되, dataset 범위와 버전 라벨을 함께 남기는 방식

## 다음 stage로 넘기는 자산

- golden set assertion
- reason code 기반 regression
- version compare input manifest

## 05-development-timeline.md와 같이 읽을 포인트

- 어떤 데이터셋과 어떤 버전 라벨을 비교하는지 먼저 고정하고 명령을 실행한다.
- dashboard stage나 capstone compare proof를 읽을 때 이 stage의 manifest 관점을 기준으로 다시 본다.

## 나중에 다시 볼 것

- 향후 precision/recall 같은 richer assertion 메트릭을 추가할 수 있다.

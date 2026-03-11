# 01 추천 품질 기준과 평가 계약 회고

## 이번 stage로 좋아진 점

- 어떤 추천이 pass인지 fail인지 문서만으로 설명할 수 있다.
- 후속 버전 비교가 같은 기준을 사용한다는 점이 분명해진다.
- 학생이 자기 프로젝트에 맞는 rubric을 설계할 출발점을 얻는다.

## 아직 약한 부분

- 별도 stage 구현이 없으므로 실제 동작은 capstone 버전으로 내려가 확인해야 한다.
- 이 단계는 '어떻게 구현했는가'보다 '무엇을 좋은 추천으로 볼 것인가'를 먼저 설명한다.

## 학생이 여기서 바로 가져갈 것

- 추천 품질 기준을 모델 설명보다 먼저 문서 계약으로 고정하는 방식
- acceptance threshold를 나중에 바꾸더라도 어떤 지표를 중심으로 볼지 먼저 합의하는 방식

## 05-development-timeline.md와 같이 읽을 포인트

- 타임라인에서 rubric 문서와 eval 경로를 먼저 읽고, 나중에 capstone eval 명령으로 내려간다.
- 이후 compare와 release gate를 읽을 때도 이 stage의 품질 계약이 기준선이라는 점을 유지한다.

## 나중에 다시 볼 것

- 추천 품질 rubric과 acceptance threshold를 문서화하는 방식
- offline eval contract를 제품 설명과 연결하는 구조

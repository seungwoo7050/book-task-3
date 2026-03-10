# 02 registry catalog와 manifest schema 회고

## 이번 stage로 좋아진 점

- catalog 데이터와 manifest 형식이 한 묶음의 계약으로 이해된다.
- 학생이 자기 프로젝트에서 seed data와 validation을 같이 설명할 수 있다.
- 후속 추천 로직이 어떤 입력 위에서 동작하는지 추적 가능하다.

## 아직 약한 부분

- 별도 stage 구현이 없으므로 실제 동작은 capstone 버전으로 내려가 확인해야 한다.
- 여기서는 추천 알고리즘보다 입력 데이터의 안정성과 검증 가능성을 먼저 설명한다.

## 학생이 여기서 바로 가져갈 것

- catalog seed와 manifest schema를 추천 알고리즘과 분리된 입력 계약으로 설명하는 방식
- validation route 자체를 품질 증빙으로 활용하는 방식

## 05-development-timeline.md와 같이 읽을 포인트

- 어떤 파일이 seed data를 정의하고 어떤 경로가 validation을 보장하는지 먼저 본다.
- capstone API나 import/export 기능을 읽을 때도 이 stage의 입력 계약 관점을 다시 적용한다.

## 나중에 다시 볼 것

- schema-first 설계와 seed data 운영 방식
- validation route를 품질 증빙으로 활용하는 방식

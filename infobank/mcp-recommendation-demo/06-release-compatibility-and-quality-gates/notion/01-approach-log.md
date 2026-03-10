# 06 release compatibility와 quality gate 접근 기록

## 이 stage의 질문

semver/compatibility gate와 release gate를 deterministic rule로 구현해 추천 시스템의 배포 판단을 설명하는 단계다. 이 설명이 실제 capstone 코드와 같은 뜻으로 읽히게 만들 수 있는가?

## 현재 레포가 택한 방향

- 별도 stage 구현을 새로 만들기보다, 실제 capstone 구현 경로를 정본으로 삼는다.
- 상위 문서 -> stage 문서 -> 연결된 capstone 경로 순서로 읽게 해, 학습 순서와 구현 경로를 분리하지 않는다.
- 실행 재현은 `v2-submission-polish` 명령을 기준으로 묶어 두고, stage 문서는 그 의미를 설명하는 역할에 집중한다.

## 이번에 버린 선택

- stage-local 가짜 구현을 추가해 실제 capstone 구조와 다른 예제를 만드는 방식
- 없는 명령이나 파일을 있는 것처럼 적는 방식
- 과거 노트만 보고 현재 구조를 추정하는 방식

## 커리큘럼 안에서의 역할

- release gate와 artifact export를 문서화하는 방식
- 배포 전 품질 점검을 추천 시스템 서사에 연결하는 방법

## 지금 열어 둔 판단

- 현재 이 stage는 문서 중심 인덱스 역할이 강하다. 필요하면 나중에 실제 mini implementation stage로 분화할 수 있다.

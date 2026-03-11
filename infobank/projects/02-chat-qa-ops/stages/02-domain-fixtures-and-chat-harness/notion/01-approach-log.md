# 02-domain-fixtures-and-chat-harness 접근 기록

## 이 stage의 질문

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?

## 선택한 방향

- fixture를 코드 안에 하드코딩하지 않고 파일로 분리했다. 이유: golden set과 replay는 사람이 diff로 검토할 수 있어야 회귀 원인 분석이 쉽다.
- deterministic harness에는 단순 keyword matching을 사용했다. 이유: stage 목표가 search quality가 아니라 재현 가능한 입력/출력 contract이기 때문이다.

## 제외한 대안

- stage pack에서 바로 Chroma나 live provider를 요구하는 방식
- replay transcript를 테스트 파일에만 넣는 방식

## 선택 기준

- 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
- fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
- 후속 golden set과 version compare 입력으로 이어질 수 있다.

## 커리큘럼 안에서의 역할

- v0의 replay harness와 seeded KB를 축소한 학습용 집중 구현본이다.
- v1/v2의 golden replay도 입력 fixture 분리가 핵심이다.

## 아직 열어 둔 판단

이 pack의 retrieval은 keyword 수준이다. 실제 capstone의 retrieval 품질을 그대로 대변하지는 않는다.

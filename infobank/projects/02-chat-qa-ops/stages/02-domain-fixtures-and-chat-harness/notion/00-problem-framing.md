# 02-domain-fixtures-and-chat-harness 문제 정의

## 이 stage가 푸는 문제

seeded knowledge base와 replay harness를 분리해 상담 품질 실험을 재현 가능한 입력 집합 위에서 수행하도록 만드는 단계다.

## 성공 기준

- 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
- fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
- 후속 golden set과 version compare 입력으로 이어질 수 있다.

## 왜 지금 이 단계를 먼저 보는가

- v0의 replay harness와 seeded KB를 축소한 학습용 집중 구현본이다.
- v1/v2의 golden replay도 입력 fixture 분리가 핵심이다.

## 먼저 알고 있으면 좋은 것

- 평가기가 답변 품질만 보지 않고 어떤 지식을 인용했는지도 확인해야 한다.

## 확인할 증거

- `python/tests/test_harness.py`가 fixture loading과 replay 결과를 검증한다.
- fixture 파일은 markdown과 JSON으로 분리되어 사람이 직접 검토하기 쉽다.

## 아직 남아 있는 불확실성

이 pack의 retrieval은 keyword 수준이다. 실제 capstone의 retrieval 품질을 그대로 대변하지는 않는다.

# 04-claim-and-evidence-pipeline 문제 정의

## 이 stage가 푸는 문제

답변에서 claim을 분리하고 각 claim에 retrieval trace와 verdict trace를 남기는 groundedness 검증 단계를 다룬다.

## 성공 기준

- 각 claim 결과에 retrieval query와 matched docs가 남는다.
- 근거가 없는 문장도 `not_found`로 기록되어 silent drop이 없다.
- 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.

## 왜 지금 이 단계를 먼저 보는가

- v1에서 추가한 claim trace, retrieval trace, verdict trace contract의 축소판이다.
- session review 페이지가 보여주는 provenance 데이터의 핵심 구조를 먼저 설명한다.

## 먼저 알고 있으면 좋은 것

- groundedness가 단순 yes/no가 아니라 문장 단위 provenance여야 한다는 점을 이해해야 한다.

## 확인할 증거

- `python/tests/test_pipeline.py`가 retrieval trace 보존을 직접 검증한다.
- pipeline은 vector DB 없이도 trace schema를 설명 가능하게 유지한다.

## 아직 남아 있는 불확실성

claim segmentation은 단순 문장 분리라 실제 복합 문장이나 함축 표현을 충분히 다루지 못한다.

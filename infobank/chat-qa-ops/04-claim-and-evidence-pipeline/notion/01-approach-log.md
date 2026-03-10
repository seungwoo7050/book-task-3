# 04-claim-and-evidence-pipeline 접근 기록

## 이 stage의 질문

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?

## 선택한 방향

- claim extraction과 evidence verification을 별도 함수로 분리했다. 이유: trace가 어느 단계에서 생성되는지 분리해야 디버깅과 교체가 쉽다.
- 근거가 없는 claim도 결과에서 제거하지 않고 `not_found`로 남긴다. 이유: 평가 파이프라인에서 빠진 claim은 향후 missing evidence failure로 연결되어야 하기 때문이다.

## 제외한 대안

- 답변 전체를 하나의 groundedness score로만 압축하는 방식
- retrieval trace 없이 evidence doc id만 남기는 방식

## 선택 기준

- 각 claim 결과에 retrieval query와 matched docs가 남는다.
- 근거가 없는 문장도 `not_found`로 기록되어 silent drop이 없다.
- 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.

## 커리큘럼 안에서의 역할

- v1에서 추가한 claim trace, retrieval trace, verdict trace contract의 축소판이다.
- session review 페이지가 보여주는 provenance 데이터의 핵심 구조를 먼저 설명한다.

## 아직 열어 둔 판단

claim segmentation은 단순 문장 분리라 실제 복합 문장이나 함축 표현을 충분히 다루지 못한다.

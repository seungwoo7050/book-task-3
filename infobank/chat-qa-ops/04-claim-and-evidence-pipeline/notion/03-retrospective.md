# 04-claim-and-evidence-pipeline 회고

## 이번 stage로 강화된 점

- session review에서 사람이 읽을 provenance data를 남길 수 있다.
- retrieval 성능 문제와 answer composition 문제를 분리해서 볼 수 있다.

## 아직 약한 부분

- confidence score나 contradiction depth는 아직 없다.

## 학생이 여기서 바로 가져갈 것

- claim을 추출한 뒤 근거 문서와 verdict trace를 끝까지 남겨, 실패 원인을 사람이 읽을 수 있게 하는 방식
- retrieval 문제와 answer composition 문제를 같은 groundedness 실패로 뭉개지 않는 방식

## 다음 stage로 넘기는 자산

- claim extraction
- retrieval trace
- verdict trace와 evidence document linkage

## 05-development-timeline.md와 같이 읽을 포인트

- pipeline 코드와 테스트를 먼저 대조하면 왜 `not_found` verdict를 버리지 않는지 이해하기 쉽다.
- capstone session review를 볼 때도 이 stage의 trace shape를 기준으로 provenance를 읽는다.

## 나중에 다시 볼 것

- 후속 실험에서 domain classification과 reranking을 trace schema에 더 붙일 수 있다.

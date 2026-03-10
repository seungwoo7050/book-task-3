# Claim & Evidence Pipeline — 회고

## 잘 된 것

### session review에서 사람이 읽을 provenance data를 남길 수 있게 됐다

claim별로 "이 문장은 KB의 어떤 문서에 근거한다"가 보이니, human reviewer가 "이건 맞는 말인가?"를 바로 확인할 수 있다.
`not_found`인 claim은 "이 문장은 KB에 근거가 없다 — 챗봇이 자체 생성한 내용이다"로 해석된다.

### retrieval 성능 문제와 answer composition 문제를 분리할 수 있게 됐다

점수가 낮을 때, "검색이 맞는 문서를 못 찾았는가"(retrieval 문제)와 "찾았는데 답변에 반영을 안 했는가"(composition 문제)를 구분할 수 있다.
retrieval trace에 검색 쿼리와 반환 문서가 함께 남기 때문이다.

## 아쉬운 것

### confidence score나 contradiction depth는 아직 없다

현재 verdict는 `support`/`not_found` 이분법이다.
"부분적으로 지지한다"나 "KB 내용과 모순된다"는 구분이 없다.

### claim segmentation이 단순 문장 분리다

마침표(`.`)와 물음표(`?`)로 split하는 것이 전부다.
"환불은 본인확인 후 접수 가능하며, 처리까지 3~5일 소요됩니다"처럼 하나의 문장에 두 개의 claim이 있는 경우를 다루지 못한다.

## 나중에 다시 볼 것

- domain classification과 reranking을 trace schema에 더 붙이면, "어떤 도메인의 문서를 선호했는가"까지 볼 수 있다.
- contradiction detection을 추가하면 "근거 있는 오답"도 잡을 수 있다.

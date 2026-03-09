# Domain Fixtures — 디버깅 기록: 한국어 질의와 문서 매칭 문제

## Case: 짧은 한국어 질의가 원하는 문서에 닿지 않음

### 증상

"환불은 몇일 걸려요?"라는 질의로 `retrieve()`를 호출했을 때, 기대한 `refund_policy.md`가 아니라 다른 문서가 top-1으로 나왔다.
더 정확히는, 어떤 문서도 점수가 0이어서 **기본값**(KB의 첫 번째 문서)이 반환됐다.

### 원인

keyword matching은 질의어와 문서 본문 단어가 **정확히 일치**해야 점수가 올라간다.
"환불"이라는 단어는 `refund_policy.md` 본문에 있지만, "몇일"이나 "걸려요"는 없었다.
질의어를 공백으로 split하면 `["환불은", "몇일", "걸려요?"]`가 되는데, "환불은"과 "환불"은 다른 단어다.

한국어의 특성상 조사("은", "는", "이", "가")가 붙으면 정확 매칭이 깨진다.

### 해결

검색 점수에 **doc_id 매칭**도 포함시켰다.
`doc_id`가 `refund_policy.md`이고 질의에 "환불"이 들어가면, `"환불" in doc_id`는 아니지만 `"환불" in content`는 참이다.
그리고 `"refund" in doc_id`는 당장 한국어 질의에서는 도움이 안 되지만, 파일명에 한국어 단어 단서가 들어가면 도움이 된다.

결과적으로 `score = sum(1 for term in query_terms if term in content or term in doc_id)`로 변경해서,
질의어 중 하나라도 문서 본문이나 파일명에 포함되면 점수가 올라가도록 만들었다.

### 검증

`test_replay_harness_reproduces_expected_docs`가 `refund_policy.md`를 top-1으로 요구한다.
이 테스트가 통과하면 "환불 관련 질의 → 환불 정책 문서"라는 최소 계약이 유지되는 것이다.

## 이 경험에서 배운 것

한국어 텍스트 검색에서 정확 매칭은 생각보다 자주 실패한다.
형태소 분석기 없이도 **파일명 힌트**를 추가하는 것만으로 fixture 수준의 재현성은 확보할 수 있었다.
하지만 이건 "stage pack 수준의 workaround"이고, 실제 capstone에서는 embedding 기반 검색으로 넘어갔다.

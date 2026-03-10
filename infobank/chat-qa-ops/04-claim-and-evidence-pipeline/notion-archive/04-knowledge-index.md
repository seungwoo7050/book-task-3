# Claim & Evidence Pipeline — 지식 인덱스

## 핵심 개념

### Claim Extraction

답변 텍스트를 **개별 주장(claim)**으로 분리하는 과정이다.
이 stage에서는 마침표와 물음표 기준의 단순 문장 분리를 사용한다.
각 claim에는 `claim_id`(예: `claim-1`)와 `statement`가 부여된다.

### Retrieval Trace

각 claim을 검증할 때 **어떤 검색 쿼리로 어떤 문서를 찾았는지** 남기는 기록이다.
trace가 있으면 "왜 이 문서가 근거로 선택됐는가"를 사후에 분석할 수 있다.
구조: `{query: string, docs: string[]}`

### Verdict Trace와 Evidence Document Linkage

verdict는 각 claim의 최종 판정이다: `support`(근거 있음) 또는 `not_found`(근거 없음).
evidence_doc_ids는 해당 claim을 지지하는 문서 목록이다.
이 둘이 함께 있어야 "왜 이 점수가 나왔는가"를 설명할 수 있다.

## 참고 자료

### Evidence Verifier Trace Shape (capstone)

- **경로**: `08-capstone-submission/v1-regression-hardening/python/backend/src/evaluator/evidence_verifier.py`
- **왜 읽었나**: capstone에서 어떤 trace 항목이 실제로 필요한지 확인하기 위해
- **배운 것**: retrieval query, returned docs, verdict, evidence ids를 **한 덩어리**로 봐야 groundedness를 설명할 수 있다
- **이후 영향**: stage 04는 retrieval trace와 verdict trace를 최소 schema로 유지

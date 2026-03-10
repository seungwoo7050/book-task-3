# Claim & Evidence Pipeline — 디버깅 기록: 근거 없는 claim이 사라지는 문제

## Case: matched docs가 없는 claim이 결과에서 누락됨

### 증상

답변에 claim이 3개 있었는데, 검증 결과에는 2개만 나왔다.
`verify_claims()` 결과의 `claim_results` 리스트 길이가 입력 claims 길이보다 짧았다.

### 원인

초기 구현에서 matched docs가 없는 claim을 결과 리스트에 추가하지 않았다.
`if matched:` 조건 안에서만 `claim_results.append()`를 호출했기 때문에, 매칭이 0인 claim은 결과에 아예 빠졌다.

이렇게 빠진 claim이 실은 **가장 중요한 실패 원인**일 수 있다.
"KB에 없는 내용을 답변이 포함했다"는 것은 groundedness 문제의 핵심이기 때문이다.

### 해결

`if matched:` 조건을 제거하고, 모든 claim에 대해 결과를 추가하도록 변경했다.
matched가 없으면 `verdict: "not_found"`, `evidence_doc_ids: []`, `retrieval_trace: {query: ..., docs: []}`로 채운다.

### 검증

`test_claim_pipeline_keeps_retrieval_trace`가 첫 번째 claim의 `verdict == "support"`와 `retrieval_trace.docs == ["refund_policy.md"]`를 검증한다.
그리고 구현에서 모든 claim이 결과 리스트에 유지되는 것은 코드 구조로 보장된다.

## 이 경험에서 배운 것

"결과가 없으면 건너뛴다"는 직관이 위험한 경우가 있다.
특히 **실패 분석**이 목적인 시스템에서는, "아무것도 못 찾았다"는 것도 하나의 유의미한 결과다.

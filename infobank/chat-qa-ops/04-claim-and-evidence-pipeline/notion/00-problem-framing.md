# Claim & Evidence Pipeline — 왜 "문장 단위 근거 추적"이 필요한가

## 출발점

"이 답변은 근거가 있나?"라는 질문에 가장 쉽게 답하는 방법은 yes/no다.
답변 전체를 KB와 비교해서 "대체로 맞다" 또는 "근거를 찾을 수 없다"라고 판정하면 된다.

하지만 실제 상담 답변은 여러 문장으로 구성된다:
- "환불은 본인확인 후 접수 가능합니다."
- "상담원 연결이 필요할 수 있습니다."

첫 번째 문장은 `refund_policy.md`에 근거가 있을 수 있지만, 두 번째 문장은 KB에 없을 수 있다.
답변 전체에 하나의 groundedness score를 매기면, **어떤 문장이 문제인지** 알 수 없다.

session review에서 사람이 "이 답변의 어디가 근거 없는 주장인가?"를 보려면, **문장(claim) 단위의 provenance**가 필요하다.

## 이 단계가 해결하려는 것

핵심 질문:

> "답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?"

목표:
1. 답변에서 claim을 분리한다.
2. 각 claim에 retrieval trace(어떤 쿼리로 어떤 문서를 찾았는지)와 verdict(`support` 또는 `not_found`)를 남긴다.
3. 근거가 없는 문장도 `not_found`로 기록해서 **silent drop이 없다**.

## 성공 기준

- 각 claim 결과에 retrieval query와 matched docs가 남는다.
- 근거가 없는 문장도 `not_found`로 기록된다.
- 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.

## 이 트랙을 처음 보는 사람을 위한 전제

- groundedness는 단순 yes/no가 아니라 **문장 단위 provenance**여야 한다.
- claim segmentation은 이 stage에서는 단순 문장 분리(마침표 기준)다. 복합 문장이나 함축 표현은 다루지 않는다.
- 이 stage는 v1에서 추가한 claim trace, retrieval trace, verdict trace contract의 **축소판**이다.

# Judge & Score Merge — 왜 "판단"과 "계산"을 나눠야 했는가

## 출발점

stage 01에서 rubric을 고정했고, stage 03에서 failure types를 정의했다.
이제 남은 건 **실제로 답변을 보고 점수를 매기는 것**이다.

가장 자연스러운 구조는 하나의 함수에서 "답변을 보고, 점수를 내고, 총점까지 계산하는 것"이다.
처음에는 그렇게 만들었다. `evaluate(user_msg, response) -> {total, grade}`로 한 번에 끝나니까.

하지만 문제는 이 함수를 **LLM judge로 교체**하려고 할 때 생겼다.
heuristic이 내는 subscore와 LLM이 내는 subscore의 **기준이 다른데**, 총점 계산 규칙까지 함께 바뀌면 "점수가 바뀐 이유가 judge 때문인지, 계산 때문인지" 구분이 안 됐다.

## 이 단계가 해결하려는 것

핵심 질문:

> "응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?"

해결: **judge는 subscore와 failure types만** 반환하고, **merge는 final score만** 계산한다.

## 성공 기준

- judge와 scorer가 별도 함수 계약을 가진다.
- failure types는 판단 결과와 최종 score 계산 모두에 반영된다.
- live provider가 없어도 deterministic 테스트가 가능하다.

## 이 트랙을 처음 보는 사람을 위한 전제

- stage 01의 weighted rubric과 stage 03의 failure taxonomy를 이미 알고 있어야 한다.
- 이 stage는 **live provider 품질**이 아니라 **interface boundary**를 보는 것이 목적이다.
- heuristic judge는 실제 상담 품질의 뉘앙스를 충분히 반영하지 못한다. stage 목적은 **interface freeze**다.

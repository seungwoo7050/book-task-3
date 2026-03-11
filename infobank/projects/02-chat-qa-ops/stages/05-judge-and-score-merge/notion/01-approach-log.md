# 05-judge-and-score-merge 접근 기록

## 이 stage의 질문

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?

## 선택한 방향

- judge는 subscore와 failure types를 만들고, merge는 final score만 계산하게 분리했다. 이유: LLM judge를 도입하더라도 final scoring contract는 별도로 검증 가능해야 하기 때문이다.
- stage pack에서는 heuristic judge를 유지했다. 이유: 외부 모델 의존성 없이도 score merge 구조를 설명하고 테스트할 수 있어야 한다.

## 제외한 대안

- judge가 총점까지 직접 반환하는 monolithic evaluator
- groundedness/compliance를 judge 내부 추정치로만 숨기는 방식

## 선택 기준

- judge와 scorer가 별도 함수 계약을 가진다.
- failure types는 판단 결과와 최종 score 계산 모두에 반영된다.
- live provider가 없어도 deterministic 테스트가 가능하다.

## 커리큘럼 안에서의 역할

- v1의 LLM judge trace와 stage01 rubric contract 사이를 잇는 중간 단계다.
- 추후 provider가 바뀌어도 merge contract는 유지된다는 점을 보여준다.

## 아직 열어 둔 판단

heuristic judge는 실제 상담 품질의 뉘앙스를 충분히 반영하지 못한다. stage 목적은 interface freeze다.

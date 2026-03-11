# 00-source-brief 접근 기록

## 이 stage의 질문

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?

## 선택한 방향

- source brief를 불변 dataclass와 상수 tuple로 표현했다. 이유: 문장형 README만으로는 이후 stage에서 baseline이나 stack이 쉽게 drift했기 때문이다.
- reference spine을 다섯 문서로 제한했다. 이유: 읽어야 할 문서 수를 최소화해 다른 사람이 repository를 빠르게 이해하도록 만들기 위해서다.

## 제외한 대안

- README 서술만 남기고 코드 계약은 만들지 않는 방식
- legacy 디렉터리 구조를 그대로 학습 sequence로 간주하는 방식

## 선택 기준

- 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.
- reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.
- 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.

## 커리큘럼 안에서의 역할

- `08/v0`를 기준점으로 삼는 이유를 stage 단위에서 먼저 고정한다.
- 이후 모든 README와 verification 문서는 이 source brief를 따라야 한다.

## 아직 열어 둔 판단

이 단계는 설계 방향을 고정할 뿐, 실제 evaluator나 dashboard가 동작함을 입증하지는 않는다.

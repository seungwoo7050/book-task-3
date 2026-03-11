# 03 Retrospective

## 이번 단계에서 얻은 것

- 같은 언어라도 evaluator, checker, VM 세 단계로 관심사를 분리하면 학습 포인트가 훨씬 선명해집니다.
- explicit capture slot과 disassembly를 남기면 "closure가 실제로 무엇을 저장하는가"를 코드와 문서 양쪽에서 설명하기 쉬워집니다.

## 일부러 남긴 단순화

- optimization pass는 넣지 않았습니다.
- global environment는 empty dict로 두고, unresolved name은 runtime path에만 남겼습니다.
- register machine이나 SSA는 다루지 않았습니다.

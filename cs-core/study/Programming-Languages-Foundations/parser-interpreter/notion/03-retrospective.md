# 03 Retrospective

## 이번 단계에서 얻은 것

- parser와 evaluator를 한 프로젝트 안에 묶으면 "문법을 읽는 법"과 "의미를 실행하는 법"을 한 번에 설명할 수 있습니다.
- 타입 주석을 지금부터 문법에 포함시켜 두면 뒤 단계에서 같은 언어를 유지하기 쉬워집니다.

## 일부러 남긴 단순화

- recursion keyword, pattern matching, tuple/list 같은 자료구조는 넣지 않았습니다.
- 정적 타입 검사는 다음 프로젝트로 미뤘습니다.
- bytecode나 VM은 아직 만들지 않았습니다.

## 다음 단계

- `static-type-checking`에서 같은 문법을 다시 파싱하고, static error를 별도 진단 표면으로 분리합니다.
- `bytecode-ir`에서 같은 AST를 다른 실행 모델로 낮춰 tree-walk interpreter와 결과를 비교합니다.

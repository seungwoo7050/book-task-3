# `iaddq`가 제어 신호 사고를 강제하는 이유

## 핵심 오해부터 정리

Part B에서 자주 하는 오해는 "명령어 하나 추가니까 코드 한두 줄만 바꾸면 되겠지"라는 생각입니다.
하지만 `iaddq V, rB`는 pipeline의 여러 단계에 동시에 흔적을 남깁니다.

## 어떤 단계가 영향을 받는가

- fetch: regid와 immediate를 함께 읽어야 한다
- decode: `rB` 값을 읽어야 한다
- execute: `valB + valC`를 계산해야 한다
- condition code: 산술 연산처럼 `ZF`, `SF`, `OF`를 갱신해야 한다
- write-back: 결과를 다시 `rB`에 써야 한다

즉, 새 명령어는 "문법"이 아니라 "데이터 흐름" 전체를 건드립니다.

## 저장소의 companion model이 하는 일

이 저장소의 C/C++ companion model은 HCL 자체를 파싱하지는 않습니다.
대신 HCL이 만들어 내야 하는 의미 결과를 명시적으로 모델링합니다.

- `next_pc = pc + 10`
- `valE = valB + valC`
- `dstE = rB`
- condition code는 결과에 맞춰 다시 계산

이렇게 하면 제어 신호 reasoning을 일반 코드와 테스트로도 다시 확인할 수 있습니다.

## 학습 포인트

Part B의 핵심은 "새 명령어를 외운다"가 아닙니다.
"한 명령어가 processor state 어디를 건드리는가"를 시스템적으로 추적하는 것입니다.

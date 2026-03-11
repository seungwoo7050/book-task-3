# Programming-Languages-Foundations

이 트랙은 parser, static typing, bytecode/VM 흐름을 작은 언어 하나로 연결해 보는 구간입니다.
문법을 읽는 법과 프로그램 의미를 설명하는 법을 동시에 익히는 것이 목표입니다.

## 누구를 위한 문서인가

- 파서와 인터프리터를 직접 구현해 보며 PL 기초 감각을 잡고 싶은 학습자
- 정적 타입 검사가 런타임 오류와 어떻게 다른지 작은 예제로 보고 싶은 사람
- AST 이후 intermediate representation과 VM까지 연결되는 최소 경로가 필요한 사람

## 필수 코어와 심화

| 순서 | 구분 | 프로젝트 | 이 단계에서 보는 질문 | 다음 단계 |
| --- | --- | --- | --- | --- |
| 1 | `필수 코어` | [`parser-interpreter`](parser-interpreter/README.md) | 토큰화, 파싱, 평가기가 한 언어 안에서 어떻게 연결되는가 | `static-type-checking` |
| 2 | `필수 코어` | [`static-type-checking`](static-type-checking/README.md) | 같은 언어에서 어떤 오류를 실행 전에 막을 수 있는가 | `bytecode-ir` |
| 3 | `심화/선택` | [`bytecode-ir`](bytecode-ir/README.md) | AST를 bytecode와 VM으로 바꾸면 실행 모델이 어떻게 달라지는가 | 더 큰 compiler/runtime 실험 |

## 공용 언어 계약

- expression-oriented, call-by-value, lexical scoping, left-to-right evaluation을 유지합니다.
- 표면 문법은 정수/불리언 literal, identifier, 괄호, unary `-`/`not`, binary operator, `let`, `if ... then ... else ...`, `fun (...) -> Type => expr`, call `f(a, b)`를 포함합니다.
- 타입 표면은 `Int`, `Bool`, 함수 타입 `T -> U`, `(T1, T2) -> U`만 지원합니다.
- 프로젝트들은 같은 언어 표면을 공유하지만 코드 의존성은 두지 않고, 각 디렉터리에서 self-contained하게 구현합니다.

## 디렉터리 구조

```text
Programming-Languages-Foundations/
  README.md
  parser-interpreter/
  static-type-checking/
  bytecode-ir/
```

## 먼저 읽을 곳

1. [`parser-interpreter/problem/README.md`](parser-interpreter/problem/README.md)
2. [`static-type-checking/problem/README.md`](static-type-checking/problem/README.md)
3. [`bytecode-ir/problem/README.md`](bytecode-ir/problem/README.md)
4. [`parser-interpreter/README.md`](parser-interpreter/README.md)
5. [`static-type-checking/README.md`](static-type-checking/README.md)
6. [`bytecode-ir/README.md`](bytecode-ir/README.md)

## 검증 방법

2026-03-11 기준으로 세 프로젝트 모두 deterministic한 테스트 명령과 demo/replay 명령을 갖고 있습니다.

- `parser-interpreter`: `python3 -m pytest`, `PYTHONPATH=src python3 -m parser_interpreter --demo all`
- `static-type-checking`: `python3 -m pytest`, `PYTHONPATH=src python3 -m static_type_checking --demo all`
- `bytecode-ir`: `python3 -m pytest`, `PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run`, `PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`

구체 명령과 성공 신호는 각 프로젝트의 `README.md`와 `notion/05-development-timeline.md`를 따르면 됩니다.

## 이 트랙을 끝내면 남는 것

- 하나의 언어 표면을 parser, checker, VM 세 단계로 나눠 설명할 수 있습니다.
- static error와 runtime error, 그리고 execution model의 차이를 같은 fixture 집합으로 비교할 수 있습니다.
- 이후 optimizer, richer type system, 더 큰 compiler/runtime 실험으로 올라갈 기준선을 얻게 됩니다.

## 공개 범위

- 세 프로젝트 모두 self-authored lab이므로 구현 코드, 테스트, `docs/`, `notion/`, `examples/`를 전부 공개 대상으로 유지합니다.
- 외부 course handout이나 비공개 바이너리에 의존하지 않으므로, README는 구현과 검증 안내에 집중합니다.

## 포트폴리오로 확장하는 힌트

- 현재 트랙은 parser, static checker, bytecode/VM까지 한 바퀴를 완료한 상태입니다.
- 개인 저장소에서는 parser trace, type error gallery, bytecode/disasm 캡처를 붙이면 세 단계 차이가 더 잘 드러납니다.
- 다음 확장은 optimizer pass, richer type system, 더 큰 compiler/runtime 실험 중 하나를 별도 프로젝트로 떼어 내는 편이 좋습니다.

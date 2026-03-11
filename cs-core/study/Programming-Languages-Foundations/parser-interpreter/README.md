# Parser Interpreter

작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행합니다.

## 이 프로젝트에서 배우는 것

- token stream과 precedence가 parser shape를 어떻게 결정하는지 익힙니다.
- `let`, `if`, `fun`, call이 lexical scope 안에서 어떻게 평가되는지 확인합니다.
- 타입 주석을 문법에 포함시키되, 실행 단계에서는 아직 사용하지 않는 구조를 경험합니다.

## 누구를 위한 문서인가

- 파서와 인터프리터를 직접 구현해 보며 PL 입문 기준선을 만들고 싶은 학습자
- `let`, `if`, closure를 실제 코드와 테스트로 연결해 보고 싶은 사람
- 뒤 단계 `static-type-checking`, `bytecode-ir`를 같은 언어로 이어 읽고 싶은 사람

## 먼저 읽을 곳

1. `problem/README.md`로 현재 범위와 deliberately omitted 항목을 먼저 확인합니다.
2. `docs/README.md`와 개념 문서를 읽어 lexer, parser, environment 용어를 맞춥니다.
3. `src/parser_interpreter/`와 `tests/test_parser_interpreter.py`를 함께 읽으며 보장 범위를 확인합니다.
4. `examples/`와 CLI demo를 실행해 source, AST, result 출력이 어떻게 이어지는지 봅니다.
5. `notion/README.md`와 `notion/05-development-timeline.md`로 재현 순서를 확인합니다.

## 디렉터리 구조

```text
parser-interpreter/
  README.md
  problem/
  docs/
  examples/
  src/parser_interpreter/
  tests/
  notion/
  notion-archive/
```

## 검증 명령

```bash
cd cs-core/study/Programming-Languages-Foundations/parser-interpreter
python3 -m pytest
PYTHONPATH=src python3 -m parser_interpreter --demo all
```

2026-03-11 기준 대표 결과:

- `tests/test_parser_interpreter.py` 11개 테스트 통과
- demo `closures` 결과 `42`
- demo `short-circuit` 결과 `1`
- demo `typed-syntax` 결과 `11`

## 공개 범위

- 이 프로젝트는 self-authored toy language lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 전부 공개 대상으로 유지합니다.
- 외부 과제 자산이나 비공개 바이너리에 의존하지 않으므로, README는 구현과 검증 안내에 집중합니다.

## 구현에서 집중할 포인트

- recursive descent 앞에 precedence climbing을 붙여 infix operator 우선순위를 안정적으로 처리하는지 봅니다.
- lexical closure가 생성된 시점의 environment를 캡처하고, call 시점 환경과 섞이지 않는지 봅니다.
- 타입 주석은 AST에 남기되 evaluator는 arity와 runtime shape만 확인하도록 경계를 나눕니다.

## 포트폴리오로 확장하는 힌트

- parser trace나 AST visualization을 붙이면 문법 설계 경험을 보여 주기 좋습니다.
- 이후 `static-type-checking`, `bytecode-ir`를 같은 언어로 이어 붙이면 "하나의 언어를 여러 실행 모델로 설명했다"는 서사가 생깁니다.

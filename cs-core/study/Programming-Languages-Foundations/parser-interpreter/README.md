# Parser Interpreter

`parser-interpreter`는 작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행하는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| 하나의 toy language에 대해 lexer, parser, evaluator를 구현하고 demo와 테스트로 결과를 재현한다. | expression-oriented 문법, lexical scoping, left-to-right evaluation을 유지하고 타입 주석은 파싱만 한다. | 구현은 [`src/parser_interpreter/`](src/parser_interpreter), [`tests/`](tests), [`examples/`](examples)와 CLI demo로 정리한다. | [`problem/README.md`](problem/README.md), [`docs/README.md`](docs/README.md) | token stream, precedence, lexical closure, tree-walk evaluation | `public verified` |

## 디렉터리 역할

- `problem/`: 범위와 의도적으로 제외한 항목
- `src/parser_interpreter/`: lexer, parser, evaluator 구현
- `tests/`: parser/evaluator acceptance test
- `examples/`: CLI demo 입력 예제
- `docs/`: recursive descent, environment, token stream 개념 정리
- `notion/`: 접근 로그와 재검증 timeline

## 검증 빠른 시작

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

## 공개 경계

- 이 프로젝트는 self-authored toy language lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 전부 공개 대상으로 유지한다.
- README는 구현과 검증 entrypoint에 집중하고, parser trace나 세부 reasoning은 `docs/`, `notion/`으로 분리한다.

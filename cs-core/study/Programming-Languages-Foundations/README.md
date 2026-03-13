# Programming-Languages-Foundations

`Programming-Languages-Foundations`는 같은 toy language를 parser, type checker, bytecode VM 세 단계로 다시 구현해 언어의 문법, 정적 규칙, 실행 모델을 함께 읽는 트랙이다.

## 프로젝트 지도

| 프로젝트 | 문제 | 이 레포의 답 | 검증 시작점 | 상태 |
| --- | --- | --- | --- | --- |
| [`parser-interpreter`](parser-interpreter/README.md) | lexer, parser, tree-walk evaluator를 한 언어로 구현 | `src/parser_interpreter`, `tests/`, `examples/` | [`problem`](parser-interpreter/problem/README.md), [`docs`](parser-interpreter/docs/README.md) | `public verified` |
| [`static-type-checking`](static-type-checking/README.md) | 같은 언어에 static type rule과 diagnostic surface 추가 | `src/static_type_checking`, `tests/`, `examples/` | [`problem`](static-type-checking/problem/README.md), [`docs`](static-type-checking/docs/README.md) | `public verified` |
| [`bytecode-ir`](bytecode-ir/README.md) | 같은 언어를 bytecode와 VM으로 lowering해 실행 모델 비교 | `src/bytecode_ir`, `tests/`, `examples/` | [`problem`](bytecode-ir/problem/README.md), [`docs`](bytecode-ir/docs/README.md) | `public verified` |

코드 기반 재구성 blog 시리즈는 [`../blog/Programming-Languages-Foundations/README.md`](../blog/Programming-Languages-Foundations/README.md)에서 모아 보고, 프로젝트별 진입점은 [Bytecode IR](../blog/Programming-Languages-Foundations/bytecode-ir/00-series-map.md), [Parser Interpreter](../blog/Programming-Languages-Foundations/parser-interpreter/00-series-map.md), [Static Type Checking](../blog/Programming-Languages-Foundations/static-type-checking/00-series-map.md) 에서 바로 읽을 수 있다.

## 권장 순서

1. [`parser-interpreter`](parser-interpreter/README.md)
2. [`static-type-checking`](static-type-checking/README.md)
3. [`bytecode-ir`](bytecode-ir/README.md)

- `필수 코어`: `parser-interpreter -> static-type-checking`
- `심화/선택`: `bytecode-ir`

## 검증 원칙

- 세 프로젝트 모두 deterministic한 `pytest`와 CLI demo 명령을 canonical verification path로 유지한다.
- 표면 문법은 공유하지만 구현은 디렉터리별 self-contained를 유지한다.
- README는 `문제`, `답`, `검증`, `공개 범위`만 짧게 설명하고, 규칙 해설과 rebuild log는 `docs/`, `notion/05-development-timeline.md`로 내린다.

## 공개 경계

- 세 프로젝트 모두 self-authored lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 공개 대상으로 유지한다.
- 외부 course handout이나 비공개 바이너리에 의존하지 않으므로, 공개 표면은 구현과 검증 안내에 집중한다.
- 같은 언어 표면을 유지하면서 execution model만 바뀐다는 점이 이 트랙의 핵심 메시지다.

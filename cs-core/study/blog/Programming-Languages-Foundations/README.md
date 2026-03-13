# Programming-Languages-Foundations 블로그 트랙

같은 함수형 언어를 세 가지 방식으로 처리하는 3개 프로젝트의 개발 타임라인.
lexer/parser를 공유하고, 위로 evaluator → type checker → compiler/VM을 쌓는다.

## 프로젝트 목록

| 프로젝트 | 핵심 주제 | 시리즈 |
|----------|-----------|--------|
| [Parser-Interpreter](parser-interpreter/) | lexer, recursive descent, closure semantics | [→](parser-interpreter/00-series-map.md) |
| [Static Type Checking](static-type-checking/) | TypeEnvironment, 함수 타입, Diagnostic | [→](static-type-checking/00-series-map.md) |
| [Bytecode IR](bytecode-ir/) | compiler, FunctionProto, stack VM, closure capture | [→](bytecode-ir/00-series-map.md) |

## 언어 설명

세 프로젝트가 처리하는 언어는 정수/불리언 리터럴, 단항/이항 연산, `let`-in, `if`-then-else, `fun` 표현식을 지원한다.
정적 타입 annotation은 선택적이며 static-type-checking에서 검사한다.

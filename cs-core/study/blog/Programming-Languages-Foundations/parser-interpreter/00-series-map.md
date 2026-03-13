# Parser Interpreter 시리즈 맵

`parser-interpreter`는 작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행하는 프로젝트다. 이 시리즈는 결과만 정리해 둔 회고문이 아니라, token stream을 먼저 고정하고, recursive descent parser와 evaluator를 올린 뒤, closure demo로 lexical scope를 닫는 흐름을 복원한다.를 끝까지 따라가게 만드는 입구다.

2026-03-13에 기존 초안을 `study/blog/_legacy/2026-03-13-isolate-and-rewrite/Programming-Languages-Foundations/parser-interpreter/`로 옮긴 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 시리즈를 다시 썼다. 그래서 이 문서는 '무엇을 만들었는가'보다 '어떤 순서로 읽어야 그 판단 이동이 보이는가'를 먼저 설명한다.

## 이 시리즈를 읽는 방법

가장 먼저 `01-evidence-ledger.md`에서 살아 있는 근거를 모아 본다. 그 다음 `_structure-outline.md`에서 왜 최종 글이 그 순서로 배치되는지 확인한다. 마지막으로 `10-2026-03-13-reconstructed-development-log.md`에서 그 근거가 실제 서사로 어떻게 이어지는지 읽는다.

## 이번 재작성에서 붙잡은 source-of-truth

- 문제 계약: [`README.md`](../../../Programming-Languages-Foundations/parser-interpreter/README.md), [`problem/README.md`](../../../Programming-Languages-Foundations/parser-interpreter/problem/README.md)
- 구현 표면: `src/parser_interpreter/__init__.py`, `src/parser_interpreter/__main__.py`, `src/parser_interpreter/ast.py`, `src/parser_interpreter/diagnostics.py`, `src/parser_interpreter/environment.py`, `src/parser_interpreter/evaluator.py`
- 검증 entrypoint: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all` in `.`
- 개념 축: `environment and closures`, `lexer and token stream`, `recursive descent and precedence`

## 읽는 순서

1. [`01-evidence-ledger.md`](01-evidence-ledger.md) — source-first 근거와 phase별 판단 전환점을 먼저 모아 둔 문서
2. [`_structure-outline.md`](_structure-outline.md) — 최종 글의 읽기 곡선과 장면 배치를 설명하는 편집 설계 메모
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md) — 구현 순서, 코드, CLI를 한 흐름으로 다시 쓴 최종 blog

## 이번에 따라간 질문

token stream을 먼저 고정하고, recursive descent parser와 evaluator를 올린 뒤, closure demo로 lexical scope를 닫는 흐름을 복원한다.

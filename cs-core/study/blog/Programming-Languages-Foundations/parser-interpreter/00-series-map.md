# Parser-Interpreter 시리즈 맵

## 프로젝트 개요

간단한 함수형 언어를 위한 lexer + parser + tree-walk interpreter.
closure semantics, `let`-in scope, 단항/이항 연산자를 지원한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | maximal munch, let 우선순위, closure environment 캡처 |

## 검증 경로

```bash
cd python && pip install -e . && pytest tests/ -v
echo "let x = 3 in x * 2" | python -m parser_interpreter
```

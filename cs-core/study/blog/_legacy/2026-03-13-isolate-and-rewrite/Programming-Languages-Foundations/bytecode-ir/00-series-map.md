# Bytecode IR 시리즈 맵

## 프로젝트 개요

parser-interpreter 언어를 bytecode로 컴파일하고 stack-based VM으로 실행.
FunctionProto, closure capture, call frame, reference evaluator와 동일한 의미를 보장한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | instruction set 설계, closure capture_sources, CompileContext resolve, VM frame |

## 검증 경로

```bash
cd python && pip install -e . && pytest tests/ -v
echo "let fact = fun (n: Int) -> Int = if n == 0 then 1 else n * fact (n - 1) in fact 5" | python -m bytecode_ir
```

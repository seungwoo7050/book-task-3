# Static Type Checking 시리즈 맵

## 프로젝트 개요

parser-interpreter 위에 얹는 Hindley-Milner 스타일 타입 체커.
TypeEnvironment scope chain, 함수 타입 checking, 에러 진단을 구현한다.

## 타임라인

| 파일 | 기간 | 핵심 내용 |
|------|------|-----------|
| [1편](10-2026-03-11.md) | 2026-03-11 | scope chain, FunExpr 타입 checking, Diagnostic line/column |

## 검증 경로

```bash
cd python && pip install -e . && pytest tests/ -v
echo "let x: Int = true in x + 1" | python -m static_type_checking
```

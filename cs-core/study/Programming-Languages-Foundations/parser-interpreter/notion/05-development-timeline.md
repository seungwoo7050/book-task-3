# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Programming-Languages-Foundations/parser-interpreter
python3 -m pytest
PYTHONPATH=src python3 -m parser_interpreter --demo all
```

## 2026-03-11 재검증 기록

- `python3 -m pytest` 결과: `11 passed`
- `PYTHONPATH=src python3 -m parser_interpreter --demo all` 결과:
  - `closures` -> `42`
  - `short-circuit` -> `1`
  - `typed-syntax` -> `11`

## 읽는 순서 메모

1. `problem/README.md`로 범위를 다시 잡습니다.
2. `docs/`로 parser/evaluator 용어를 맞춥니다.
3. `tests/`를 먼저 읽어 이 프로젝트가 무엇을 보장하는지 확인합니다.
4. 마지막으로 demo를 실행해 source/AST/result 출력 형식을 눈으로 확인합니다.

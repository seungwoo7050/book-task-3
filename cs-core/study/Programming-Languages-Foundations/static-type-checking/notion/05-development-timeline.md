# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Programming-Languages-Foundations/static-type-checking
python3 -m pytest
PYTHONPATH=src python3 -m static_type_checking --demo all
```

## 2026-03-11 재검증 기록

- `python3 -m pytest` 결과: `13 passed`
- `PYTHONPATH=src python3 -m static_type_checking --demo all` 결과:
  - `higher-order` -> `Int`
  - `let-inference` -> `Int`
  - `typed-branching` -> `Int`

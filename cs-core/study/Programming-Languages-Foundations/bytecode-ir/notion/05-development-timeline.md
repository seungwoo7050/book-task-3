# 05 Development Timeline

## 재구축 순서

```bash
cd cs-core/study/Programming-Languages-Foundations/bytecode-ir
python3 -m pytest
PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run
PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm
```

## 2026-03-11 재검증 기록

- `python3 -m pytest` 결과: `9 passed`
- `PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run` 결과:
  - `closure-pipeline` -> `42`
  - `disasm-sample` -> `9`
  - `higher-order` -> `12`
- `PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm` 결과:
  - module function과 nested lambda의 instruction offset이 stable text로 출력됨

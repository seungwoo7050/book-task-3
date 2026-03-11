# 04 Knowledge Index

## 핵심 파일

- `../src/bytecode_ir/compiler.py`
- `../src/bytecode_ir/vm.py`
- `../src/bytecode_ir/reference_evaluator.py`
- `../tests/test_bytecode_ir.py`

## 핵심 개념 문서

- `../docs/concepts/stack-machine-model.md`
- `../docs/concepts/call-frame-and-closure.md`
- `../docs/concepts/bytecode-disassembly.md`

## 검증 앵커

- equivalence/disassembly 테스트: `../tests/test_bytecode_ir.py`
- run entry point: `../src/bytecode_ir/__main__.py`
- replay fixture: `../examples/closure-pipeline.plf`, `../examples/disasm-sample.plf`, `../examples/higher-order.plf`

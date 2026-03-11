# 00 Problem Framing

## 핵심 질문

- 같은 AST를 tree-walk 대신 stack machine으로 실행하려면 어떤 최소 instruction set이 필요한가?
- lexical closure를 VM에서 explicit capture slot으로 어떻게 드러낼 수 있는가?
- lowering 결과를 어떻게 stable text로 남겨 테스트와 문서 근거로 동시에 쓸 수 있는가?

## 성공 기준

- VM이 representative program에서 reference evaluator와 같은 결과를 낸다.
- disassembler golden이 핵심 lowering shape를 고정한다.
- closure capture와 jump 기반 short-circuit가 테스트로 검증된다.

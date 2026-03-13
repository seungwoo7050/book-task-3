# Programming-Languages-Foundations 블로그 트랙

작은 함수형 언어를 parser, type checker, bytecode VM으로 차례로 다시 구현하는 트랙이다. 같은 언어 표면을 유지한 채 실행 모델만 바뀔 때 무엇이 달라지는지, 그리고 그 차이를 어떤 진단·테스트·demo로 보여 줄 수 있는지를 따라간다.

이 트랙의 문서는 모두 같은 원칙을 따른다. 프로젝트별 `00-series-map.md`에서 읽는 순서를 잡고, `01-evidence-ledger.md`에서 근거를 확인한 뒤, `_structure-outline.md`와 최종 blog로 넘어간다. `_legacy`는 비교용 보관소일 뿐 현재 시리즈의 입력 근거가 아니다.

## 프로젝트 가이드

### [Bytecode IR](bytecode-ir/)

`bytecode-ir`는 같은 toy language를 stack-based bytecode로 낮춘 뒤 작은 VM으로 실행해 표면 문법은 유지한 채 실행 모델만 바꾸는 프로젝트다.

- 시리즈 입구: [bytecode-ir/00-series-map.md](bytecode-ir/00-series-map.md)
- 핵심 질문: 같은 언어 표면을 유지한 채 compiler와 VM을 올리고, reference evaluator/disassembler로 lowering 결과를 확인하는 흐름을 복원한다.
- 대표 검증 명령: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`

### [Parser Interpreter](parser-interpreter/)

`parser-interpreter`는 작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행하는 프로젝트다.

- 시리즈 입구: [parser-interpreter/00-series-map.md](parser-interpreter/00-series-map.md)
- 핵심 질문: token stream을 먼저 고정하고, recursive descent parser와 evaluator를 올린 뒤, closure demo로 lexical scope를 닫는 흐름을 복원한다.
- 대표 검증 명령: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`

### [Static Type Checking](static-type-checking/)

`static-type-checking`은 같은 toy language를 다시 파싱한 뒤 runtime에 넘기기 전에 어떤 오류를 미리 거를 수 있는지 정리하는 프로젝트다.

- 시리즈 입구: [static-type-checking/00-series-map.md](static-type-checking/00-series-map.md)
- 핵심 질문: parser surface를 유지한 채 type environment와 checker를 얹고, runtime 전에 어떤 오류를 끊어낼 수 있는지 demo로 닫는 흐름을 복원한다.
- 대표 검증 명령: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`

## 공통 문서 구조

- `00-series-map.md` — 왜 이 프로젝트를 이런 순서로 읽어야 하는지 설명하는 입구
- `01-evidence-ledger.md` — source-first 근거와 phase별 코드/CLI 앵커를 모아 둔 문서
- `_structure-outline.md` — 최종 글의 장면 배치와 전환 문장을 정리한 편집 메모
- `10-2026-03-13-reconstructed-development-log.md` — 구현 순서와 검증 신호를 하나의 서사로 다시 쓴 최종 blog

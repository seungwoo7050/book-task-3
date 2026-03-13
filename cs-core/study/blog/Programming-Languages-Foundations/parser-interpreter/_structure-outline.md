# Parser Interpreter Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Parser Interpreter에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 lexer와 token stream contract를 먼저 만든다 -> Phase 2 recursive descent parser와 evaluator로 lexical scope를 연결한다 -> Phase 3 demo program과 pytest로 언어 표면을 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - lexer와 token stream contract를 먼저 만든다

이 구간의 중심 장면은 파서 프로젝트도 결국 가장 먼저 흔들리면 안 되는 것은 token boundary다.

본문에서는 먼저 문법 오류를 parser에서 다루기 전에 `tokenize_source`가 identifier, number, keyword를 안정적으로 자르는 쪽이 우선이라고 봤다. 그 다음 문단에서는 lexer와 token definition을 먼저 고정해 parser가 기대할 입력 표면을 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `tokenize_source`, `Token`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 강조할 검증 신호: token stream이 먼저 있으니 parser 오류를 문법 문제로 좁힐 수 있다.
- 장면이 끝날 때 남길 문장: recursive descent parser로 precedence를 얹는다.

## 2. Phase 2 - recursive descent parser와 evaluator로 lexical scope를 연결한다

이 구간의 중심 장면은 `parse_source`, `evaluate_source`, environment helper가 같은 언어 surface를 두 단계로 나눠 설명한다.

본문에서는 먼저 parser와 evaluator를 강하게 결합하면 closure와 short-circuit reasoning이 흐려질 것 같아 AST를 중심으로 단계를 분리했다. 그 다음 문단에서는 precedence-aware parser를 만든 뒤 environment/closure evaluator를 separate module로 유지했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `evaluate_source`, `parse_source`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 강조할 검증 신호: parser/evaluator 분리가 글에서도 판단 이동을 자연스럽게 보여 준다.
- 장면이 끝날 때 남길 문장: demo program과 pytest로 표면을 닫는다.

## 3. Phase 3 - demo program과 pytest로 언어 표면을 닫는다

이 구간의 중심 장면은 언어 프로젝트는 내부 AST보다 sample program 결과가 더 직접적인 검증 신호가 된다.

본문에서는 먼저 examples와 CLI demo가 남아 있어야 closure, short-circuit, typed syntax parsing을 한 번에 재생할 수 있다고 판단했다. 그 다음 문단에서는 `python3 -m pytest`와 `--demo all` entrypoint를 남겨 parser/evaluator 경로를 반복 실행 가능하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `main`, `test_closure_uses_lexical_scope`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 강조할 검증 신호: pytest와 demo output이 최종 검증 신호를 남긴다.
- 장면이 끝날 때 남길 문장: token stream -> AST/evaluator -> demo verification 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.

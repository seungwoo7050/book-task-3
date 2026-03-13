# Static Type Checking Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Static Type Checking에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 같은 언어 표면을 다시 파싱 가능한 AST로 유지한다 -> Phase 2 type environment와 rule checking을 별도 층으로 만든다 -> Phase 3 demo와 pytest로 static/runtime 경계를 보여 준다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - 같은 언어 표면을 다시 파싱 가능한 AST로 유지한다

이 구간의 중심 장면은 type checker도 parser가 달라지면 앞 프로젝트와 연결 고리가 끊어진다.

본문에서는 먼저 새 프로젝트지만 parser surface는 최대한 유지하고 type annotation 해석만 덧붙이는 편이 학습 연결이 좋다고 봤다. 그 다음 문단에서는 parser/AST를 공유 가능한 형태로 다시 세우고, checker가 기대할 입력 표면을 유지했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `parse_source`, `TypeExpr`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 강조할 검증 신호: shared syntax가 있으니 parser-interpreter와 대비되는 지점이 선명해진다.
- 장면이 끝날 때 남길 문장: type environment와 rule checking으로 이동한다.

## 2. Phase 2 - type environment와 rule checking을 별도 층으로 만든다

이 구간의 중심 장면은 `check_expression`, `_expect_exact_type`, function type helper가 이 프로젝트의 핵심 전환점이다.

본문에서는 먼저 runtime evaluator처럼 값을 계산하기보다 environment에 타입을 축적하는 규칙을 따로 세워야 오류를 미리 잡을 수 있다고 판단했다. 그 다음 문단에서는 type environment, exact-type assertion, function application rule을 checker에 모아 static rule layer를 구성했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `check_expression`, `_expect_exact_type`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 강조할 검증 신호: checker helper가 rule별 판단 이동을 함수 수준으로 보존한다.
- 장면이 끝날 때 남길 문장: demo program과 pytest로 static/runtime 경계를 닫는다.

## 3. Phase 3 - demo와 pytest로 static/runtime 경계를 보여 준다

이 구간의 중심 장면은 type checker는 통과 프로그램과 실패 프로그램을 함께 보여 줄 때 가장 설명력이 크다.

본문에서는 먼저 CLI demo와 pytest가 있으면 '어떤 오류를 미리 자르는가'를 한 번에 재현할 수 있다고 봤다. 그 다음 문단에서는 `--demo all`과 tests를 통해 higher-order, branching, let inference 케이스를 반복 확인하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `main`, `test_accepts_higher_order_program`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 강조할 검증 신호: pytest와 demo output이 마지막 검증 신호를 남긴다.
- 장면이 끝날 때 남길 문장: shared parser -> type environment -> diagnostic demo 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/static-type-checking && python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.

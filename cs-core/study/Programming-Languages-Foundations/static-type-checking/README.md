# Static Type Checking

같은 toy language를 다시 파싱한 뒤, runtime에 넘기기 전에 어떤 오류를 미리 거를 수 있는지 정리하는 프로젝트입니다.

## 이 프로젝트에서 배우는 것

- operator, `if`, function call, return boundary에서 어떤 type rule이 필요한지 익힙니다.
- lexical scope와 별도로 type environment가 왜 필요한지 확인합니다.
- parser는 같아도 error surface를 runtime이 아니라 static diagnostic으로 바꿀 수 있다는 점을 봅니다.

## 누구를 위한 문서인가

- `parser-interpreter` 다음 단계에서 static rule을 추가로 보고 싶은 학습자
- type environment와 function boundary를 작은 예제로 이해하고 싶은 사람
- runtime error와 static error를 같은 문법 위에서 비교해 보고 싶은 사람

## 먼저 읽을 곳

1. `problem/README.md`로 현재 checker가 맡는 범위를 확인합니다.
2. `docs/README.md`와 개념 문서로 static/runtime 경계를 먼저 맞춥니다.
3. `src/static_type_checking/`와 `tests/test_static_type_checking.py`를 함께 읽습니다.
4. `examples/`와 CLI demo로 acceptance path를 다시 실행합니다.
5. `notion/README.md`와 `notion/05-development-timeline.md`로 재검증 순서를 확인합니다.

## 디렉터리 구조

```text
static-type-checking/
  README.md
  problem/
  docs/
  examples/
  src/static_type_checking/
  tests/
  notion/
  notion-archive/
```

## 검증 명령

```bash
cd cs-core/study/Programming-Languages-Foundations/static-type-checking
python3 -m pytest
PYTHONPATH=src python3 -m static_type_checking --demo all
```

2026-03-11 기준 대표 결과:

- `tests/test_static_type_checking.py` 13개 테스트 통과
- demo `higher-order`, `let-inference`, `typed-branching` 모두 최종 타입 `Int`

## 공개 범위

- 이 프로젝트는 self-authored type checking lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 전부 공개 대상으로 유지합니다.
- 외부 비공개 자산은 없고, 검증은 전부 현재 저장소 안의 fixture와 문서화된 명령으로 재현됩니다.

## 구현에서 집중할 포인트

- parameter와 return boundary를 function type의 최소 계약으로 고정했는지 봅니다.
- optional `let` annotation은 "주석이 없으면 추론, 있으면 검증"으로 처리되는지 확인합니다.
- runtime에서만 알 수 있는 오류와 static 단계에서 이미 막을 수 있는 오류를 섞지 않는지 봅니다.

## 포트폴리오로 확장하는 힌트

- error gallery와 reject fixture 설명을 붙이면 type system 사고를 훨씬 읽기 쉽게 보여 줄 수 있습니다.
- 이후 `bytecode-ir`와 연결하면 "같은 언어의 문법, 타입, 실행 모델"을 한 시퀀스로 설명할 수 있습니다.

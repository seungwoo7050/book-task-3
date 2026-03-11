# Static Type Checking

`static-type-checking`은 같은 toy language를 다시 파싱한 뒤 runtime에 넘기기 전에 어떤 오류를 미리 거를 수 있는지 정리하는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| parser 이후 단계에서 static type rule과 diagnostic surface를 추가해 실행 전 오류를 걸러낸다. | language surface는 유지하고, `let` annotation은 optional, type environment와 runtime environment를 섞지 않는다. | 구현은 [`src/static_type_checking/`](src/static_type_checking), [`tests/`](tests), [`examples/`](examples)와 CLI demo로 정리한다. | [`problem/README.md`](problem/README.md), [`docs/README.md`](docs/README.md) | type environment, function type, static diagnostic, runtime/static 경계 | `public verified` |

## 디렉터리 역할

- `problem/`: checker 범위와 의도적으로 제외한 항목
- `src/static_type_checking/`: parser 재사용부와 type checker 구현
- `tests/`: accept/reject fixture와 diagnostic 테스트
- `examples/`: CLI demo 입력 예제
- `docs/`: static/runtime 경계, function rule, type environment 정리
- `notion/`: 접근 로그와 재검증 timeline

## 검증 빠른 시작

```bash
cd cs-core/study/Programming-Languages-Foundations/static-type-checking
python3 -m pytest
PYTHONPATH=src python3 -m static_type_checking --demo all
```

2026-03-11 기준 대표 결과:

- `tests/test_static_type_checking.py` 13개 테스트 통과
- demo `higher-order`, `let-inference`, `typed-branching` 모두 최종 타입 `Int`

## 공개 경계

- 이 프로젝트는 self-authored type checking lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 전부 공개 대상으로 유지한다.
- README는 검증 entrypoint와 현재 scope를 먼저 보여 주고, type rule 세부 설명은 `docs/`, `notion/`으로 분리한다.

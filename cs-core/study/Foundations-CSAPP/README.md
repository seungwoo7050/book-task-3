# Foundations-CSAPP

`Foundations-CSAPP`는 비트 표현, ISA, 캐시, 역공학을 한 줄기 학습 경로로 묶어 CS:APP 핵심 lab를 다시 읽는 트랙이다.

## 프로젝트 지도

| 프로젝트 | 문제 | 이 레포의 답 | 검증 시작점 | 상태 |
| --- | --- | --- | --- | --- |
| [`datalab`](datalab/README.md) | 제한된 연산자와 상수만으로 `bits.c` 13개 퍼즐 구현 | `c/src/bits.c`, `cpp/src/bits.cpp`, `docs/` | [`problem`](datalab/problem/README.md), [`c`](datalab/c/README.md), [`cpp`](datalab/cpp/README.md) | `verified (local-only asset)` |
| [`archlab`](archlab/README.md) | Y86 작성, `iaddq` 제어 로직, `ncopy` 성능 개선 | `y86/src/*.ys`, `c/src/mini_archlab.c`, `cpp/src/mini_archlab.cpp` | [`problem`](archlab/problem/README.md), [`y86`](archlab/y86/README.md), [`c`](archlab/c/README.md) | `verified (local-only asset)` |
| [`bomblab`](bomblab/README.md) | phase별 입력 조건을 assembly에서 복원 | `c/src/mini_bomb.c`, `cpp/src/mini_bomb.cpp`, `docs/` | [`problem`](bomblab/problem/README.md), [`c`](bomblab/c/README.md), [`cpp`](bomblab/cpp/README.md) | `verified (local-only asset)` |
| [`attacklab`](attacklab/README.md) | code injection, ROP, 상대 주소 계산 이해 | `c/src/mini_attacklab.c`, `cpp/src/mini_attacklab.cpp`, `docs/` | [`problem`](attacklab/problem/README.md), [`c`](attacklab/c/README.md), [`cpp`](attacklab/cpp/README.md) | `verified (local-only asset)` |
| [`perflab`](perflab/README.md) | cache simulator와 cache-friendly transpose 구현 | `c/src/perflab.c`, `cpp/src/perflab.cpp`, `docs/` | [`problem`](perflab/problem/README.md), [`c`](perflab/c/README.md), [`cpp`](perflab/cpp/README.md) | `public verified` |

## 권장 순서

1. [`datalab`](datalab/README.md)
2. [`archlab`](archlab/README.md)
3. [`bomblab`](bomblab/README.md)
4. [`attacklab`](attacklab/README.md)
5. [`perflab`](perflab/README.md)

- `필수 코어`: `datalab -> archlab`
- `심화/선택`: `bomblab -> attacklab`, `perflab`

## 검증 원칙

- `datalab`, `archlab`, `bomblab`, `attacklab`은 `problem/`에서 공식 자산을 로컬에 복원한 뒤 `make verify-official`로 전체 경계를 확인한다.
- 공개 구현 검증은 각 프로젝트의 `c/`, `cpp/`, `y86/` README가 canonical entrypoint가 된다.
- 세부 명령과 상태 정의는 루트 [`docs/status-matrix.md`](../docs/status-matrix.md), [`docs/readme-contract.md`](../docs/readme-contract.md)를 따른다.

## 공개 경계

- 공개 README는 `문제`, `답`, `검증`, `공개 범위`만 짧게 보여 주고, 긴 reasoning은 프로젝트 `docs/`, `notion/`으로 내린다.
- `bomblab`, `attacklab`은 workflow와 개념 설명 중심으로 유지하고, course-instance 전용 raw answer나 exploit은 저장소에 두지 않는다.
- `problem/` 아래 공식 starter와 verifier는 원문 계약 보존이 우선이다.

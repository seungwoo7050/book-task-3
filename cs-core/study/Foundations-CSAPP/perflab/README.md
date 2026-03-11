# Performance Lab

`perflab`은 cache simulator와 transpose 최적화를 통해 "왜 더 빠른가"를 코드와 지표로 설명하는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| Part A는 trace-driven cache simulator, Part B는 cache-friendly transpose 구현이다. | trace 입력과 miss 집계 규칙을 지키고, transpose는 correctness와 miss budget을 함께 만족해야 한다. | C 답은 [`c/src/perflab.c`](c/src/perflab.c), C++ 답은 [`cpp/src/perflab.cpp`](cpp/src/perflab.cpp)이며, miss 근거와 전략 비교는 `docs/`에 둔다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | cache model, LRU, trace-driven 검증, blocking 전략 | `public verified` |

## 디렉터리 역할

- `problem/`: self-written starter boundary와 sample trace
- `c/`, `cpp/`: simulator와 transpose 구현
- `docs/`: cache model, LRU, transpose strategy 설명
- `notion/`: 최적화 과정, 실패 사례, 재측정 기록

## 검증 빠른 시작

문제 경계 확인:

```bash
cd problem
make status
make compile
```

C 구현 검증:

```bash
cd c
make clean && make test
```

C++ 구현 검증:

```bash
cd cpp
make clean && make test
```

## 공개 경계

- 공개 문서는 cache model과 최적화 전략을 설명한다.
- 특정 코드 블록 전체를 해답처럼 붙여 넣기보다, miss를 줄이는 원리를 중심으로 정리한다.
- `problem/`은 self-written starter boundary만 유지한다.

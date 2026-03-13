# Malloc Lab

`malloclab`은 힙 블록 레이아웃, 정렬 규칙, explicit free list, coalescing, `realloc`을 한 번에 다루는 allocator 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `malloc`, `free`, `realloc` 계약을 만족하는 동적 메모리 할당기를 구현한다. | alignment, block metadata, free list invariant를 지켜야 하고, starter contract는 `problem/`에서만 유지한다. | C 답은 [`c/src/mm.c`](c/src/mm.c), C++ 답은 [`cpp/src/mm.cpp`](cpp/src/mm.cpp), 개념 해설은 `docs/`와 `notion/`으로 분리한다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | allocator invariant, coalescing, free list, `realloc` payload 보존 | `public verified` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Systems-Programming/malloclab/00-series-map.md`](../../blog/Systems-Programming/malloclab/00-series-map.md)

## 디렉터리 역할

- `problem/`: starter contract와 최소 컴파일 경계
- `c/`, `cpp/`: allocator 구현과 테스트
- `docs/`: block layout, coalescing, `realloc` reasoning 정리
- `notion/`: 실패 사례와 재현 로그

## 검증 빠른 시작

문제 경계 확인:

```bash
cd problem
make clean && make
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

- 공개 문서는 allocator 불변식과 검증 전략을 설명한다.
- 구현 전체를 장문으로 복붙하기보다, 블록 레이아웃과 free list 정책을 중심으로 정리한다.
- 외부 비공개 자산이 없으므로 구현 코드와 테스트를 공개 대상으로 유지한다.

# Malloc Lab

## 이 프로젝트가 가르치는 것

`malloclab`은 힙 블록 레이아웃, 정렬 규칙, explicit free list, coalescing, `realloc`의 의미를 한 번에 다루게 하는 프로젝트입니다.
API는 작지만, 메모리 관리자의 불변식을 어떻게 세우고 지키는지가 핵심입니다.

## 누구를 위한 문서인가

- 동적 메모리 할당기를 직접 구현해 보고 싶은 학습자
- `malloc`, `free`, `realloc`의 관계를 trace 기반으로 검증하고 싶은 사람
- 자료구조 선택과 메모리 레이아웃 설계를 함께 설명하고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`c/README.md`](c/README.md)
3. [`cpp/README.md`](cpp/README.md)
4. [`docs/README.md`](docs/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
malloclab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

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

## 스포일러 경계

- 공개 문서는 allocator 불변식과 검증 전략을 설명합니다.
- 구현 전체를 장문으로 복붙하기보다, 블록 레이아웃과 free list 정책을 중심으로 정리합니다.
- 이 프로젝트는 외부 비공개 자산이 없으므로 공개 범위가 비교적 넓습니다.

## 포트폴리오로 확장하는 힌트

- 이 프로젝트는 "자료구조를 왜 이렇게 골랐는가"를 설명할 수 있을 때 가치가 높아집니다.
- 개인 저장소에서는 block diagram과 `realloc` 확장 경로 그림을 추가하면 이해도가 크게 올라갑니다.

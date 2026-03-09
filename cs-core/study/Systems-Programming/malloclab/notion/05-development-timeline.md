# Malloc Lab — 개발 타임라인

이 문서는 소스 코드에 드러나지 않는 개발 과정의 시간 순서, 사용한 CLI 명령, 환경 구축 절차를 기록한다.

---

## Phase 1: 문제 환경 준비

### problem/ 구성

1. `problem/code/memlib.c`, `memlib.h` — 힙 시뮬레이션 모듈 배치
2. `problem/code/mm.c`, `mm.h` — TODO 스켈레톤 배치
3. `problem/script/mdriver.c` — 강화된 트레이스 드라이버 작성

### 트레이스 작성

`problem/data/traces/` 아래 4개 `.rep` 파일을 직접 작성:
- `basic.rep` (8 ids, 12 ops) — malloc/free 기본
- `coalesce.rep` (10 ids, 18 ops) — 병합 압박
- `realloc.rep` (6 ids, 14 ops) — realloc 전 경로
- `mixed.rep` (12 ids, 22 ops) — 혼합 시나리오

### 빌드 확인

```bash
cd problem
make clean && make
```

---

## Phase 2: C 트랙 구현

### 디렉터리 설정

```
c/
  Makefile
  include/mm.h, memlib.h
  src/mm.c
```

Makefile이 `../problem/code/memlib.c`와 `../problem/script/mdriver.c`를 참조하여 같은 드라이버를 공유한다.

### 구현 순서

1. 블록 레이아웃 헬퍼 (`align_size`, `pack`, `load_word`, `store_word`, `header_of`, `footer_of`, `next_block`, `previous_block`)
2. Free-list 포인터 접근 (`next_free_slot`, `prev_free_slot`)
3. Free-list 조작 (`add_to_free_list`, `remove_from_free_list`)
4. `coalesce` — 4-way 분기
5. `extend_heap` — prologue/epilogue 관리
6. `mm_init` — 초기 힙 레이아웃 (padding + prologue + epilogue + 4KB extend)
7. `find_fit` — first-fit 순회
8. `place_block` — 할당 + 분할
9. `mm_malloc`, `mm_free`
10. `mm_realloc` — shrink-split, in-place growth, fallback copy

### 검증

```bash
cd c
make clean && make test
# → ./build/mdriver -t ../problem/data/traces -v
```

결과:
- basic.rep, coalesce.rep, realloc.rep, mixed.rep — 모두 errors=0
- avg_util=0.077, throughput≈4,691,933 ops/s

---

## Phase 3: C++ 트랙

### 구현

C 트랙과 동일한 알고리즘을 C++ 관용구로 재작성:
- `#define` → `constexpr`
- C 캐스트 → `static_cast` / `reinterpret_cast`
- `static` 전역 → anonymous namespace
- `extern "C"` 래퍼로 mm_* 인터페이스 노출

Makefile에서 `memlib.c`와 `mdriver.c`를 `-x c++` 플래그로 C++ 컴파일한다.

### 검증

```bash
cd cpp
make clean && make test
```

결과:
- 4개 트레이스 모두 errors=0
- throughput≈5,033,165 ops/s

---

## Phase 4: 문서 작성

### docs/ 구성

- `docs/concepts/allocator-invariants.md` — 블록 레이아웃, 정렬, free-list 불변식, 정합성 검사 항목
- `docs/concepts/realloc-and-coalescing.md` — 즉시 병합 근거, placement 정책, realloc 3단계 전략
- `docs/references/verification.md` — 빌드 명령, 검증 커버리지, 현재 결과 (util, throughput, errors)

---

## 의존성 요약

| 항목 | 내용 |
|---|---|
| 컴파일러 | gcc (C99), g++ (C++20) |
| 빌드 | make |
| 외부 라이브러리 | 없음 |
| 힙 시뮬레이션 | `memlib.c` (256MB `malloc` 버퍼) |
| 트레이스 | 직접 작성, `problem/data/traces/` |
| Docker | 불필요 (순수 POSIX) |
| 로컬 환경 | macOS |

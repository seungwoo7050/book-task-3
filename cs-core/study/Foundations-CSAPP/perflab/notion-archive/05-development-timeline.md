# Performance Lab — 개발 타임라인

이 문서는 소스 코드에 드러나지 않는 개발 과정의 시간 순서, 사용한 CLI 명령, 환경 구축 절차를 기록한다.

---

## Phase 1: 문제 환경 준비

### starter 파일 구성

`problem/code/` 디렉토리에 자체 작성한 starter 파일 배치:
- `csim.c` — 캐시 시뮬레이터 스켈레톤
- `trans.c` — 전치 함수 스켈레톤
- `cachelab.c`, `cachelab.h` — 헬퍼 함수

### 검증 트레이스 작성

`problem/data/traces/study.trace` 작성. 공식 트레이스를 재배포하지 않고, 자체 트레이스로 시뮬레이터를 검증한다.

### starter 컴파일 체크

```bash
cd study/Foundations-CSAPP/perflab/problem
make compile
```

`csim-starter`와 `trans-starter.o`가 에러 없이 빌드되는 것을 확인.

---

## Phase 2: C 컴패니언 — 캐시 시뮬레이터

### 구현

`c/src/perflab.c`에 `CacheSim` 구조체 기반 캐시 시뮬레이터 구현:
- `cache_sim_init()`: 세트와 라인 배열 할당
- `cache_access()`: 주소 분해 → hit/miss/eviction 판정 → LRU 갱신
- `perflab_run_trace_file()`: 트레이스 파일 파싱 + 시뮬레이션

### 검증

```bash
cd study/Foundations-CSAPP/perflab/c
make clean && make test
```

`study.trace`에 대해 세 구성의 기대값 일치 확인:
- s=1, E=1, b=1 → hits:5, misses:10, evictions:8
- s=2, E=1, b=2 → hits:6, misses:9, evictions:7
- s=5, E=1, b=5 → hits:10, misses:5, evictions:0

---

## Phase 3: C 컴패니언 — 전치 최적화

### 계측 프레임워크 구현

`TransposeCache` 구조체로 s=5, E=1, b=5 직접 매핑 캐시 시뮬레이션:
- `load_a()`, `store_b()`, `load_b()` — 주소 계산 + 캐시 접근 래퍼
- A는 주소 0, B는 주소 1MB 오프셋
- `perflab_measure_transpose()` — 매트릭스 할당 + 커널 실행 + 정확성/미스 측정

### 나이브 전치 구현

```c
// perflab_transpose_naive()
for (i = 0; i < N; ++i)
    for (j = 0; j < M; ++j)
        B[j][i] = A[i][j];
```

### 32×32 최적화

- 8×8 블로킹 + 대각선 지연 쓰기 구현
- 결과: 284 misses (임계값 300)

### 64×64 최적화

- 3단계 사분면 전략 구현 (상단 전체 → 교환 → 하단 우측)
- 결과: 1,176 misses (임계값 1,300)

### 61×67 최적화

- 16×16 일반 블로킹 + 경계 가드
- 결과: 1,989 misses (임계값 2,000)

### 전체 검증

```bash
cd c
make clean && make test
```

모든 크기에서 정확성 + 미스 임계값 + naive 대비 개선 확인.

---

## Phase 4: C++ 컴패니언

### 구현

C 트랙과 동일한 로직을 C++ 스타일로 재구현:
- `std::vector` 기반 매트릭스
- 네임스페이스 `perflab::`
- 동일한 캐시 시뮬레이터 + 계측 프레임워크

### 검증

```bash
cd study/Foundations-CSAPP/perflab/cpp
make clean && make test
```

C 트랙과 동일한 결과 확인.

---

## Phase 5: 문서 작성

### docs/ 구성

- `docs/concepts/cache-sim-lru.md` — 캐시 시뮬레이터 핵심 교훈과 검증 정책
- `docs/concepts/transpose-strategies.md` — 세 크기별 전략 비교
- `docs/references/verification.md` — 검증 명령과 현재 결과

---

## 의존성 요약

| 항목 | 내용 |
|---|---|
| 컴파일러 | gcc (C11), g++ (C++17) |
| 빌드 | make |
| 검증 트레이스 | `problem/data/traces/study.trace` (자체 작성) |
| 캐시 파라미터 | s=5, E=1, b=5 (공식 환경 동일) |
| 외부 의존성 | 없음 (Docker 불필요, 네이티브 빌드) |
| 로컬 환경 | macOS Apple Silicon |

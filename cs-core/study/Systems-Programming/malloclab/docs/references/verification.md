# Malloc Lab 검증 기록

## starter boundary 확인

```bash
cd problem
make clean && make
```

2026-03-10 기준 기록:

- starter allocator contract가 컴파일된다
- 실제 기능 검증은 C/C++ 구현 트랙에서 수행한다

## shared driver가 확인하는 것

이 저장소의 driver는 다음 항목을 본다.

- 16-byte alignment
- live payload overlap 여부
- `realloc` prefix 데이터 보존
- trace별 오류 수
- 요약 utilization과 throughput

즉, 단순 crash test보다 강한 검증을 수행합니다.

## C 구현 검증

```bash
cd c
make clean && make test
```

trace 구성:

- `basic.rep`
- `coalesce.rep`
- `realloc.rep`
- `mixed.rep`

기록:

- 네 trace 모두 `errors=0`
- summary: `avg_util=0.077`, `throughput=4691933 ops/s`

## C++ 구현 검증

```bash
cd cpp
make clean && make test
```

기록:

- 네 trace 모두 `errors=0`
- summary: `avg_util=0.077`, `throughput=5033165 ops/s`

## 현재 판단

이 저장소는 allocator를 "돌아간다" 수준이 아니라,
정렬과 `realloc` 의미까지 검증 가능한 수준으로 유지하고 있습니다.

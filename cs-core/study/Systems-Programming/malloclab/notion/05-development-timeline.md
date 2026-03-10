# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `malloclab`을 다시 구현할 때 allocator 불변식과 trace 기반 검증을 어떤 순서로 맞춰야 하는지 보존하는 재현 문서입니다.
처음부터 `realloc`으로 들어가지 않고, 규칙을 쌓아 가는 순서를 유지하는 것이 핵심입니다.

## 권장 재현 순서

1. `problem/`에서 starter boundary가 정상 컴파일되는지 먼저 확인한다.
2. `c/`에서 free list, split, coalesce, `realloc`을 포함한 전체 드라이버를 통과시킨다.
3. `cpp/` 구현도 같은 trace 기반 기준으로 다시 검증한다.
4. 수치가 흔들리면 util과 throughput보다 payload preservation과 alignment부터 다시 본다.

## 최소 명령

```bash
cd problem
make clean && make

cd ../c
make clean && make test

cd ../cpp
make clean && make test
```

## 성공 신호

- starter boundary가 정상 컴파일된다.
- C/C++ driver 모두 crash 없이 trace를 끝까지 돈다.
- alignment, overlap, payload preservation 검사가 통과한다.
- 현재 기록 기준 summary가 `avg_util=0.077`이고 throughput은 C `4691933 ops/s`, C++ `5033165 ops/s` 수준과 크게 어긋나지 않는다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: starter boundary와 trace/driver 구성
- `../docs/concepts/allocator-invariants.md`: 반드시 지켜야 할 계약
- `../docs/concepts/realloc-and-coalescing.md`: `realloc`과 병합 판단
- `../docs/references/verification.md`: 현재 검증 기록과 수치

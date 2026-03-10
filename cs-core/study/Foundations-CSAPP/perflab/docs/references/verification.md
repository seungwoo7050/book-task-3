# Performance Lab 검증 기록

## starter boundary 확인

```bash
cd problem
make status
make compile
```

2026-03-10 기준 기록:

- starter 파일과 `study.trace`가 존재한다
- starter compile check가 통과한다
- 실제 성능 판단은 C/C++ 구현 트랙에서 수행한다

## C 구현 검증

```bash
cd c
make clean && make test
```

검증 기준:

- cache simulator가 `study.trace`의 oracle을 맞춘다
- transpose가 `32x32`, `64x64`, `61x67` 모두 정답을 만든다
- optimized miss가 naive보다 낮다
- miss 목표는 각각 `<300`, `<1300`, `<2000`

기록:

- `s=1 E=1 b=1` -> `hits=5 misses=10 evictions=8`
- `s=2 E=1 b=2` -> `hits=6 misses=9 evictions=7`
- `s=5 E=1 b=5` -> `hits=10 misses=5 evictions=0`
- `32x32`: `284` misses
- `64x64`: `1176` misses
- `61x67`: `1989` misses

## C++ 구현 검증

```bash
cd cpp
make clean && make test
```

기록:

- cache simulator oracle 결과가 C track과 동일하다
- transpose miss 결과가 C track과 동일하다

## 현재 판단

이 저장소는 성능 과제를 "설명 가능한 miss 기준"으로 다시 실행 가능하게 보존하고 있습니다.

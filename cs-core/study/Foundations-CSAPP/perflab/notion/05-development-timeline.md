# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `perflab`을 다시 구현할 때 cache simulator와 transpose 최적화를 어떤 순서로 검증해야 하는지 보존하는 재현 문서입니다.
성능 과제를 단순한 점수표가 아니라 반복 가능한 측정 흐름으로 남기는 것이 목적입니다.

## 권장 재현 순서

1. `problem/`에서 starter 경계와 compile check를 먼저 확인한다.
2. `c/`에서 simulator oracle과 transpose miss 목표를 통과시킨다.
3. `cpp/`에서도 같은 결과를 다시 확인한다.
4. miss 수치가 바뀌면 `docs/references/verification.md`와 함께 원인을 기록한다.

## 최소 명령

```bash
cd problem
make status
make compile

cd ../c
make clean && make test

cd ../cpp
make clean && make test
```

## 성공 신호

- starter boundary가 정상 컴파일된다.
- simulator oracle 결과가 문서 기록과 일치한다.
- transpose miss가 `32x32 < 300`, `64x64 < 1300`, `61x67 < 2000` 기준을 만족한다.
- C/C++ 구현의 miss 결과가 서로 크게 다르지 않다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: starter boundary와 trace 위치
- `../docs/concepts/cache-sim-lru.md`: simulator state reasoning
- `../docs/concepts/transpose-strategies.md`: diagonal 처리와 blocking 전략
- `../docs/references/verification.md`: 현재 miss 수치 기록

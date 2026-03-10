# Architecture Lab 검증 기록

## 공식 self-study toolchain 검증

```bash
cd problem
make restore-official
make verify-official
```

2026-03-10 기준 기록:

- Part A Y86 프로그램이 기대 결과 `0xcba`를 만든다
- Part B SEQ `iaddq` 변경이 공식 회귀 테스트를 통과한다
- Part C PIPE `iaddq` 회귀, `ncopy` 정합성, benchmark가 Docker에서 실행된다
- 최근 Part C 결과는 `Average CPE 9.16`, `Score 26.8/60.0`이다

복원 toolchain은 `problem/official/` 아래 로컬 전용으로만 유지합니다.

## C companion 검증

```bash
cd c
make clean && make test
```

기록:

- Part A/B/C 의미 모델 테스트 통과
- optimized pseudo-CPE가 baseline보다 낮다
- companion sample run이 정상 동작한다

## C++ companion 검증

```bash
cd cpp
make clean && make test
```

기록:

- C track과 같은 의미 모델 테스트 통과
- optimized pseudo-CPE가 baseline보다 낮다

## 현재 판단

공식 hand-in 검증과 공개 companion model 검증이 모두 살아 있는 상태입니다.

# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `archlab`을 다시 따라갈 때 공식 toolchain 복원과 companion model 검증을 어떤 순서로 묶어야 하는지 보존하는 재현 문서입니다.
Part A/B/C를 한 번에 섞지 않고, 단계별로 다시 세우는 것을 목표로 합니다.

## 권장 재현 순서

1. `problem/`에서 공식 simulator/HCL toolchain을 복원하고 검증한다.
2. Part A/B/C 결과를 `docs/references/verification.md` 기준과 비교한다.
3. `c/` companion model을 테스트로 통과시킨다.
4. `cpp/` 구현을 같은 기준으로 다시 검증한다.

## 최소 명령

```bash
cd problem
make restore-official
make verify-official

cd ../c
make clean && make test

cd ../cpp
make clean && make test
```

## 성공 신호

- Part A Y86 프로그램 결과가 `0xcba`로 맞는다.
- Part B SEQ `iaddq` 변경이 공식 회귀 테스트를 통과한다.
- Part C PIPE 회귀와 benchmark가 실행된다.
- 현재 기록 기준 `Average CPE 9.16`, `Score 26.8/60.0`과 크게 어긋나지 않는다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: 공식 toolchain 복원 경계
- `../docs/concepts/part-split.md`: Part A/B/C 분리 기준
- `../docs/concepts/iaddq-and-control-signals.md`: 제어 신호 수정 범위
- `../docs/concepts/pipeline-cost-model.md`: 성능 수치 해석
- `../docs/references/verification.md`: 현재 검증 기록

# Architecture Lab

`archlab`은 Y86-64 프로그램 작성, 제어 로직 구현, 파이프라인 성능 개선을 한 흐름으로 묶는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| Part A는 Y86 프로그램 작성, Part B는 `iaddq`와 control signal 구현, Part C는 `ncopy` 성능 최적화가 핵심이다. | 공식 simulator/HCL toolchain은 로컬 복원이 필요하고, Part A/B/C 산출물을 같은 README에서 섞지 않는다. | 제출 가능한 Y86 답은 [`y86/src/*.ys`](y86/src), companion 모델은 [`c/src/mini_archlab.c`](c/src/mini_archlab.c), [`cpp/src/mini_archlab.cpp`](cpp/src/mini_archlab.cpp)로 정리한다. | [`problem/README.md`](problem/README.md), [`y86/README.md`](y86/README.md), [`c/README.md`](c/README.md), [`cpp/README.md`](cpp/README.md) | ISA 읽기, control signal, pipeline cost model, throughput 최적화 | `verified (local-only asset)` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Foundations-CSAPP/archlab/00-series-map.md`](../../blog/Foundations-CSAPP/archlab/00-series-map.md)

## 디렉터리 역할

- `problem/`: 공식 handout, simulator, HCL toolchain 경계
- `y86/`: Part A와 Part C hand-in 산출물
- `c/`, `cpp/`: 파트별 동작을 재현하는 companion 모델
- `docs/`: part split, control signal, pipeline cost model 정리
- `notion/`: 구현 순서, 실패 사례, 재검증 기록

## 검증 빠른 시작

공식 self-study handout 검증:

```bash
cd problem
make restore-official
make verify-official
```

C companion 검증:

```bash
cd c
make clean && make test
```

C++ companion 검증:

```bash
cd cpp
make clean && make test
```

## 공개 경계

- 공개 문서는 part 분해, 제어 신호 사고법, 성능 모델을 설명한다.
- 공식 simulator/HCL toolchain은 `problem/official/` 아래 로컬에서만 복원한다.
- README는 문제와 답의 위치를 설명하고, 세부 reasoning은 `docs/`와 `notion/`으로 분리한다.

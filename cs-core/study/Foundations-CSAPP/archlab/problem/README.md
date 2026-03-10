# Architecture Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 Architecture Lab의 세 파트를 공식 문제 경계로 보존합니다.
Part A는 Y86-64 어셈블리, Part B는 `iaddq` 제어 로직, Part C는 `ncopy` 성능 최적화에 해당합니다.

## 누구를 위한 문서인가

- 공식 self-study handout 복원 경로가 필요한 학습자
- `y86/` hand-in 산출물과 복원 toolchain의 관계를 알고 싶은 사람
- 공개 가능한 파일과 로컬 전용 자산을 구분하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`code/README.md`](code/README.md)
3. [`script/README.md`](script/README.md)
4. [`../y86/README.md`](../y86/README.md)

## 디렉터리 구조

```text
problem/
  README.md
  Makefile
  code/
    README.md
  script/
    README.md
```

## 검증 방법

```bash
cd problem
make restore-official
make verify-official
```

## 스포일러 경계

- 공식 toolchain과 템플릿은 `problem/official/` 아래 로컬에서만 복원합니다.
- 공개 트리에는 학습자가 직접 작성한 hand-in 산출물과 경계 설명만 남깁니다.

## 포트폴리오로 확장하는 힌트

- multi-part 프로젝트는 파트별 산출물과 검증 경로를 분리해 적을수록 이해하기 쉽습니다.

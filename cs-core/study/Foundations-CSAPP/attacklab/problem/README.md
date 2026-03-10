# Attack Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 Attack Lab의 공식 문제 계약과 공개 가능한 자산 경계를 보존합니다.
핵심은 `ctarget`과 `rtarget`의 차이를 이해하고, payload를 구조적으로 설계하는 것입니다.

## 누구를 위한 문서인가

- 공개 self-study target을 로컬에 복원해 보고 싶은 학습자
- 문제 계약과 companion verifier의 경계를 나눠 보고 싶은 사람
- 보안 과제 공개 범위를 안전하게 관리하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`code/README.md`](code/README.md)
3. [`../docs/README.md`](../docs/README.md)
4. [`script/run_attack.sh`](script/run_attack.sh)

## 디렉터리 구조

```text
problem/
  README.md
  Makefile
  code/
    README.md
    farm.c
  data/
    phase1.txt
    phase2.txt
    phase3.txt
    phase4.txt
    phase5.txt
  script/
    run_attack.sh
```

## 검증 방법

```bash
cd problem
make restore-official
make verify-official
```

## 스포일러 경계

- 공개 self-study target에 대한 검증 흐름은 설명합니다.
- 비공개 course target의 raw exploit string은 공개하지 않습니다.
- 복원 타깃과 쿠키 파일은 `problem/official/` 아래 로컬 전용 자산입니다.

## 포트폴리오로 확장하는 힌트

- 보안 프로젝트는 "무엇을 공개하지 않기로 했는가"를 명확히 적는 것만으로도 저장소 품질이 올라갑니다.

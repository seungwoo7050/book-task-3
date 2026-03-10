# Architecture Lab 스크립트 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 공식 simulator workflow가 공개 트리 바깥에서 어떻게 복원되는지 설명합니다.

## 누구를 위한 문서인가

- `make restore-official` 이후 어떤 경로를 보게 되는지 알고 싶은 사람
- 공개 스크립트와 로컬 복원 스크립트의 경계를 이해하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`../../y86/README.md`](../../y86/README.md)

## 디렉터리 구조

```text
script/
  README.md
```

## 검증 방법

```bash
cd ..
make restore-official
make verify-official
```

복원 후 공식 helper scripts는 `../official/archlab-handout/sim/` 아래에서 사용합니다.

## 스포일러 경계

- 공개 README는 workflow 위치만 설명합니다.
- 공식 helper script 본문은 로컬 복원 자산으로만 다룹니다.

## 포트폴리오로 확장하는 힌트

- 외부 도구 의존성이 강한 프로젝트는 "복원 경로 안내 README"를 따로 두면 유지보수가 쉬워집니다.

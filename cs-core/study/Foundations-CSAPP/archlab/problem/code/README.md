# Architecture Lab 문제 코드 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 공개 트리에 공식 hand-in 원본을 넣지 않고도 검증 경계를 설명하는 역할을 합니다.

## 누구를 위한 문서인가

- `y86/`와 공식 simulator tree의 관계를 빠르게 확인하고 싶은 사람
- 어떤 파일이 추적 대상인지 알고 싶은 사람

## 먼저 읽을 곳

1. [`../../y86/README.md`](../../y86/README.md)
2. [`../README.md`](../README.md)

## 디렉터리 구조

```text
code/
  README.md
```

## 검증 방법

```bash
cd ..
make restore-official
make verify-official
```

복원 후 `../../problem/official/` 아래 simulator tree에 `../../y86/` 산출물이 복사됩니다.

## 스포일러 경계

- 이 디렉터리는 경계 설명만 포함합니다.
- 공식 handout 내부 파일은 공개 트리에 커밋하지 않습니다.

## 포트폴리오로 확장하는 힌트

- hand-in 파일이 따로 있는 프로젝트는 "산출물 위치"와 "복원 위치"를 분리해 적는 편이 좋습니다.

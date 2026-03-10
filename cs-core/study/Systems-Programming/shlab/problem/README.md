# Shell Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 Shell Lab의 문제 계약을 self-written 형태로 보존합니다.
공식 starter shell, traces, driver는 공개 트리에서 제거하고, 계약과 공개 경계만 남깁니다.

## 누구를 위한 문서인가

- 공식 starter 없이도 과제 목적을 먼저 파악하고 싶은 학습자
- 어떤 자산을 제거했고 무엇으로 대체했는지 알고 싶은 사람
- 공개 가능한 문제 경계 문서를 설계하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`code/README.md`](code/README.md)
3. [`data/README.md`](data/README.md)
4. [`script/README.md`](script/README.md)

## 디렉터리 구조

```text
problem/
  README.md
  Makefile
  code/
    README.md
  data/
    README.md
  script/
    README.md
```

## 검증 방법

```bash
cd problem
make status
```

실제 실행 가능한 검증은 [`../c/README.md`](../c/README.md), [`../cpp/README.md`](../cpp/README.md), `../tests/` 아래 self-owned 경로를 따릅니다.

## 스포일러 경계

- 공개 트리에는 문제 계약만 남기고, 공식 starter 자산은 싣지 않습니다.
- README는 제거 이유와 대체 경로를 설명하는 데 집중합니다.

## 포트폴리오로 확장하는 힌트

- 외부 starter를 제거한 프로젝트는 "무엇을 어떻게 대체했는가"를 적어 두면 공개 전략이 명확해집니다.

# Performance Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 Performance Lab의 공식 starter boundary를 self-written 형태로 유지합니다.
Part A는 trace-driven cache simulator, Part B는 cache-friendly transpose가 핵심입니다.

## 누구를 위한 문서인가

- 구현 전에 문제 계약과 제공 파일을 먼저 보고 싶은 학습자
- 공식 자산 없이도 공개 가능한 starter boundary를 만들고 싶은 사람
- sample trace와 driver의 역할을 알고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`data/traces/README.md`](data/traces/README.md)
3. [`../docs/README.md`](../docs/README.md)

## 디렉터리 구조

```text
problem/
  README.md
  Makefile
  code/
    csim.c
    trans.c
    cachelab.h
    cachelab.c
  data/
    traces/
      README.md
      study.trace
  script/
    driver.py
```

## 검증 방법

```bash
cd problem
make status
make compile
```

## 스포일러 경계

- 공개 트리에는 self-written starter와 sample trace만 둡니다.
- 공식 course trace 자산은 그대로 복사하지 않습니다.

## 포트폴리오로 확장하는 힌트

- 성능 과제는 starter boundary와 실구현 경계를 분리해 두면 읽는 사람이 구조를 빨리 이해합니다.

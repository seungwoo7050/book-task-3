# Proxy Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 프록시의 문제 계약과 starter boundary를 보존합니다.
절대형 `GET` 요청 파싱, server 연결, 응답 전달, 작은 object cache가 핵심 계약입니다.

## 누구를 위한 문서인가

- 프록시 구현 전에 기본 계약과 제약을 확인하고 싶은 학습자
- shared helper와 driver wrapper의 역할을 알고 싶은 사람
- 구현 디렉터리와 문제 경계를 분리하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `code/csapp.h`

## 디렉터리 구조

```text
problem/
  README.md
  code/
    proxy.c
    csapp.c
    csapp.h
  script/
    driver.sh
  Makefile
```

## 검증 방법

```bash
cd problem
make clean && make
```

실제 프록시 동작 검증은 [`../c/README.md`](../c/README.md), [`../cpp/README.md`](../cpp/README.md), `../tests/` 경로를 따릅니다.

## 스포일러 경계

- 이 프로젝트는 self-owned 테스트 자산을 함께 공개합니다.
- README는 문제 계약과 기본 제약에 집중합니다.

## 포트폴리오로 확장하는 힌트

- 네트워크 프로젝트는 starter boundary와 테스트 harness를 명확히 나누면 이해가 쉬워집니다.

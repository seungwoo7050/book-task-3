# Proxy Lab C++ 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 C 구현과 같은 프록시 계약을 C++로 다시 구현합니다.
동시성, header rewrite, cache 정책을 다른 언어 스타일로 비교하는 경로입니다.

## 누구를 위한 문서인가

- C와 C++ 프록시 구현을 비교하고 싶은 학습자
- C++로 네트워크/스레드 코드를 정리하는 예시가 필요한 사람
- 동일 계약의 이중 구현을 보고 싶은 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../problem/README.md`](../problem/README.md)
3. `../tests/run_proxy_tests.sh`

## 디렉터리 구조

```text
cpp/
  README.md
  src/
    proxy.cpp
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- README는 구현 범위와 검증 흐름만 설명합니다.
- 세부 동기화 reasoning은 `docs/`에서 다룹니다.

## 포트폴리오로 확장하는 힌트

- 네트워크 프로젝트에서 언어별 차이를 정리하면 저장소 품질이 눈에 띄게 좋아집니다.

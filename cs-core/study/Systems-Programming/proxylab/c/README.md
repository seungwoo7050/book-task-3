# Proxy Lab C 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 HTTP/1.0 `GET` forwarding, detached thread 처리, mutex-protected LRU cache를 C로 구현합니다.
네트워크 I/O와 동시성, 캐시 정책을 함께 다루는 핵심 구현 경로입니다.

## 누구를 위한 문서인가

- C로 프록시를 직접 구현해 보고 싶은 학습자
- header rewrite와 cache hit 검증을 함께 보고 싶은 사람
- 로컬 origin server 기반 네트워크 테스트 구조가 필요한 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `../tests/run_proxy_tests.sh`

## 디렉터리 구조

```text
c/
  README.md
  src/
    proxy.c
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test
```

## 스포일러 경계

- README는 기능 범위와 테스트 경로만 설명합니다.
- 세부 캐시 전략과 동시성 reasoning은 `docs/`로 분리합니다.

## 포트폴리오로 확장하는 힌트

- 프록시 프로젝트는 요청 흐름도와 캐시 hit 시나리오를 한 장으로 정리하면 좋습니다.

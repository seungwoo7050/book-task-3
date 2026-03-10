# Proxy Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 프록시의 request forwarding, concurrency hazard, cache 정책을 공개 문서로 정리합니다.
코드만 읽으면 놓치기 쉬운 네트워크 흐름과 잠금 정책을 설명하는 역할입니다.

## 누구를 위한 문서인가

- 프록시 구현 전에 전체 데이터 흐름을 먼저 보고 싶은 학습자
- 동시성과 캐시 정책을 글로 정리하고 싶은 사람
- 테스트 하네스와 구현 코드를 연결해서 읽고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/http-forwarding.md`](concepts/http-forwarding.md)
2. [`concepts/concurrency-and-cache.md`](concepts/concurrency-and-cache.md)
3. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    http-forwarding.md
    concurrency-and-cache.md
  references/
    verification.md
```

## 검증 방법

- 상세 명령은 [`references/verification.md`](references/verification.md)에 있습니다.
- 실제 실행은 [`../c/README.md`](../c/README.md), [`../cpp/README.md`](../cpp/README.md), `../tests/`를 함께 읽습니다.

## 스포일러 경계

- 공개 문서는 흐름과 정책을 설명합니다.
- 특정 구현 파일 전체를 답안처럼 다시 싣지는 않습니다.

## 포트폴리오로 확장하는 힌트

- 네트워크 문서는 request path와 cache path를 분리해 설명하면 훨씬 읽기 쉬워집니다.

# Proxy Lab 검증 기록

## starter boundary 확인

```bash
cd problem
make clean && make
```

2026-03-10 기준 기록:

- starter proxy contract가 컴파일된다
- 실제 기능 검증은 C/C++ 구현과 shared harness에서 수행한다

## shared harness가 확인하는 것

이 저장소의 local origin server와 shell harness는 다음을 본다.

- 기본 local GET forwarding
- required header rewriting
- 작은 응답의 cache hit
- oversized object 비캐시 처리
- 두 slow request의 동시 처리
- upstream failure 뒤에도 계속 동작하는지

## C 구현 검증

```bash
cd c
make clean && make test
```

기록:

- `make test` 통과
- 기본 forwarding과 header rewrite 확인
- 두 번째 요청에서 small object cache hit 확인
- oversized object는 다시 가져오는 것 확인
- failed upstream 이후에도 proxy가 계속 사용 가능함

## C++ 구현 검증

```bash
cd cpp
make clean && make test
```

기록:

- C track과 같은 forwarding, header, cache, concurrency, failure recovery 검증 통과

## 현재 판단

이 저장소는 공식 grading server 없이도,
프록시의 핵심 기능과 동시성 정책을 충분히 설명 가능한 수준으로 검증하고 있습니다.

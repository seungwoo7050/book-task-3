# 05. 개발 타임라인

## 이 문서의 역할

이 문서는 `proxylab`을 다시 구현할 때 forwarding, cache, concurrency를 외부 서버 없이 어떤 순서로 검증해야 하는지 보존하는 재현 문서입니다.
프록시의 핵심은 기능 데모보다 반복 가능한 하네스에 있으므로, 그 순서를 먼저 남깁니다.

## 권장 재현 순서

1. `problem/`에서 starter boundary가 컴파일되는지 먼저 확인한다.
2. `c/`에서 local origin harness 기준 forwarding, header rewrite, cache, failure recovery를 통과시킨다.
3. `cpp/`에서 같은 검증 경로를 다시 확인한다.
4. 동시성 문제가 의심되면 느린 요청 두 개와 cache lock 경로부터 다시 본다.

## 최소 명령

```bash
cd problem
make clean && make

cd ../c
make clean && make test

cd ../cpp
make clean && make test
```

## 성공 신호

- starter boundary가 정상 컴파일된다.
- 기본 local GET forwarding과 required header rewrite가 확인된다.
- 작은 객체는 두 번째 요청에서 cache hit가 난다.
- oversized object는 캐시에 넣지 않고 다시 가져온다.
- 두 slow request가 함께 처리되고, upstream failure 뒤에도 proxy가 계속 동작한다.

## 재현이 어긋날 때 먼저 볼 곳

- `problem/README.md`: starter boundary와 공개 helper 범위
- `../docs/concepts/http-forwarding.md`: 요청 파싱과 헤더 정규화
- `../docs/concepts/concurrency-and-cache.md`: thread/cache 정책
- `../docs/references/verification.md`: 현재 하네스가 확인하는 항목

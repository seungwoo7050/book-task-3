# Proxy Lab 문제지

## 왜 서버 개발자에게 중요한가

이 랩은 네트워크 서버의 기본기 네 가지를 한 번에 묶어 준다.

- 소켓 기반 I/O
- HTTP 요청/응답 흐름 이해
- 동시 연결 처리
- 메모리 캐시 설계

## 목표

단일 origin server 앞에서 동작하는 concurrent HTTP proxy를 구현하라.
클라이언트의 절대형 `GET` 요청을 받아 origin으로 전달하고, 응답을 다시 클라이언트에 돌려줘야 한다.
작은 응답은 in-memory cache에 저장해 재사용한다.

## 시작 위치

- 문제 경계: `study/Systems-Programming/proxylab/problem/`
- starter 코드: `study/Systems-Programming/proxylab/problem/code/proxy.c`
- 공용 helper: `study/Systems-Programming/proxylab/problem/code/csapp.c`
- 공용 helper 헤더: `study/Systems-Programming/proxylab/problem/code/csapp.h`
- 검증 스크립트: `study/Systems-Programming/proxylab/tests/run_proxy_tests.sh`

## starter code 사용법

이 문제는 starter code가 있다.
가장 간단한 시작 방법은 `study/Systems-Programming/proxylab/problem/` 안에서 바로 작업하는 것이다.

핵심 파일 역할:

- `code/proxy.c`: 네가 채워야 하는 메인 구현 파일
- `code/csapp.c`
- `code/csapp.h`

권장 흐름:

1. `code/proxy.c`의 `TODO`를 기준으로 요청 파싱, forwarding, cache를 단계적으로 채운다.
2. `make`로 바이너리 `proxy`를 만든다.
3. `../tests/run_proxy_tests.sh ./proxy`로 동작을 검증한다.

즉, 처음엔 `problem/code/proxy.c` 하나를 중심으로 보면 된다.

## 제출물 성격

실행 형식은 아래와 같아야 한다.

```bash
./proxy <listen-port>
```

## 반드시 만족해야 하는 기능 요구사항

1. 클라이언트의 absolute-form `GET` 요청을 읽는다.

예시:

```text
GET http://127.0.0.1:18080/cacheable/basic HTTP/1.1
```

2. URI에서 아래 값을 정확히 분리한다.

- host
- port, 없으면 `80`
- path, 없으면 `/`

3. origin server로 보낼 outbound request는 `HTTP/1.0`으로 정규화한다.

요청 라인 예시:

```text
GET /cacheable/basic HTTP/1.0
```

4. 아래 헤더는 프록시가 직접 다시 써야 한다.

- `Host`
- `User-Agent`
- `Connection: close`
- `Proxy-Connection: close`

고정 `User-Agent` 값:

```text
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) Gecko/20120305 Firefox/10.0.3
```

5. 위 네 개를 제외한 다른 헤더는 필요한 경우 origin으로 전달한다.

6. origin의 응답 본문과 헤더를 클라이언트에게 그대로 스트리밍한다.

7. 여러 클라이언트 연결을 동시에 처리할 수 있어야 한다.
느린 요청 두 개가 들어와도 한 요청이 다른 요청 전체를 직렬화해서는 안 된다.

8. 작은 응답은 캐시에 저장한다.

- 단일 객체 최대 크기: `102400` bytes
- 전체 캐시 최대 크기: `1048576` bytes

9. 캐시 한도를 넘는 큰 객체는 캐시하지 않아도 되지만, 응답 전달 자체는 정상 동작해야 한다.

10. malformed request, unsupported method, upstream connection failure가 발생해도 프록시 프로세스가 죽으면 안 된다.

## 이번 문제에서 일부러 제외한 범위

- `POST`
- `CONNECT`
- HTTPS tunneling
- persistent connection
- full RFC-complete proxy behavior
- lock-free cache

## 추천 구현 순서

1. 순차적인 forwarding부터 완성한다.
2. 그 위에 thread 기반 concurrent handling을 얹는다.
3. 마지막에 cache hit, miss, eviction을 붙인다.

## 성공 체크리스트

- URI를 `host`, `port`, `path`로 안정적으로 분리할 수 있다.
- `HTTP/1.1` 요청을 받아도 origin으로는 `HTTP/1.0`으로 보낸다.
- `Host`, `User-Agent`, `Connection`, `Proxy-Connection`을 프록시 정책대로 재작성한다.
- 반복 요청에서 작은 객체는 메모리 캐시에서 다시 제공된다.
- 큰 객체는 전달되지만 캐시에 들어가지 않는다.
- 느린 요청 둘을 동시에 처리해도 전체 시간이 비정상적으로 늘어나지 않는다.

## 검증 방법

starter 경계만 컴파일:

```bash
cd study/Systems-Programming/proxylab/problem
make clean && make
```

내가 만든 프록시 바이너리 검증:

```bash
cd study/Systems-Programming/proxylab/problem
../tests/run_proxy_tests.sh ./proxy
```

## 스포일러 경계

아래는 답안 구현이므로 먼저 풀어볼 때는 열지 않는 것을 권한다.

- `study/Systems-Programming/proxylab/c/src/proxy.c`
- `study/Systems-Programming/proxylab/cpp/src/proxy.cpp`
- `study/Systems-Programming/proxylab/notion/`
- `study/blog/Systems-Programming/proxylab/`

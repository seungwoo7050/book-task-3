# Proxy Lab — 접근 기록

## 마일스톤 1: 순차 HTTP 전달

### URI 파싱

프록시가 가장 먼저 하는 일은 클라이언트의 요청 라인을 파싱하는 것이다:

```
GET http://127.0.0.1:18080/cacheable/basic HTTP/1.1
```

여기서 `http://`를 건너뛰고, 호스트(`127.0.0.1`), 포트(`18080`, 없으면 `80`), 경로(`/cacheable/basic`)를 추출한다. `strchr`와 `memchr`로 `:`, `/` 구분자를 찾는 수동 파싱이다.

핵심 에지 케이스: 포트가 생략되면 80으로 기본값 설정. 경로가 없으면 `/`로 기본값 설정.

### 요청 재구성

파싱한 정보로 원본 서버에 보낼 요청을 새로 작성한다:

```
GET /cacheable/basic HTTP/1.0\r\n
Host: 127.0.0.1:18080\r\n
User-Agent: Mozilla/5.0 ...\r\n
Connection: close\r\n
Proxy-Connection: close\r\n
\r\n
```

HTTP/1.1 → HTTP/1.0 다운그레이드, `Connection: close` 강제. 클라이언트가 보낸 `Host`, `User-Agent`, `Connection`, `Proxy-Connection`은 무시하고 프록시가 결정한 값으로 대체. 그 외 헤더(`X-Test` 등)는 그대로 전달.

이 재구성을 `build_request()`에서 `append_line()` 유틸리티로 안전하게 버퍼에 누적한다. 버퍼 오버플로 방지를 위해 매번 남은 용량을 체크한다.

### 전달 흐름

1. 원본 서버에 `open_clientfd(host, port)` 연결
2. 재구성한 요청을 `rio_writen(serverfd, request, ...)`으로 전송
3. 응답을 `rio_readnb()`로 읽으면서 동시에 클라이언트에 `rio_writen(clientfd, ...)`으로 전달
4. 원본 연결 닫기

이 "읽으면서 쓰는" 파이프라인이 프록시의 핵심이다.

## 마일스톤 2: 동시 처리

### 스레드 모델

```c
while (1) {
    int *clientfd = malloc(sizeof(int));
    *clientfd = accept(listenfd, ...);
    pthread_create(&tid, NULL, thread_main, clientfd);
}
```

요청마다 새 스레드를 생성하는 가장 단순한 모델이다. `pthread_detach(pthread_self())`로 자원 회수를 자동화한다.

핵심 결정: `clientfd`를 힙에 할당해서 포인터로 전달. 스택 변수의 주소를 전달하면, 메인 루프가 다음 `accept()`로 넘어갈 때 값이 덮어씌워진다.

### SIGPIPE 무시

```c
signal(SIGPIPE, SIG_IGN);
```

클라이언트가 응답을 받기 전에 연결을 끊으면, `rio_writen()`에서 `SIGPIPE`가 발생한다. 이것을 무시하지 않으면 프록시 전체가 종료된다.

## 마일스톤 3: LRU 캐시

### 자료 구조

이중 연결 리스트 + 뮤텍스:

```
cache_head ↔ entry ↔ entry ↔ ... ↔ cache_tail
```

각 엔트리는 URI(키), 응답 데이터(값), 크기, prev/next 포인터를 가진다.

### cache_lookup 흐름

1. 뮤텍스 락 획득
2. 리스트 순회하면서 URI 매칭
3. 히트: 엔트리를 리스트 헤드로 승격(promote), 데이터 복사, 락 해제
4. 미스: 락 해제, NULL 반환

**중요**: 락을 쥔 채 클라이언트에 쓰지 않는다. 데이터를 복사한 뒤 락을 해제하고, 복사본을 클라이언트에 전달한다. 이것이 캐시 락 점유 시간을 최소화하는 핵심 설계다.

### cache_store 흐름

1. 객체 크기가 `MAX_OBJECT_SIZE`(100KB)를 초과하면 캐싱하지 않음
2. 새 엔트리 할당, 데이터 복사
3. 뮤텍스 락 획득
4. 총 캐시 크기가 `MAX_CACHE_SIZE`(1MB)를 초과하면 `cache_tail`(LRU)부터 반복 eviction
5. 새 엔트리를 리스트 헤드에 삽입
6. 락 해제

### 캐싱 가능 판정

응답을 읽으면서 동시에 `object_buf`에 누적한다. `MAX_OBJECT_SIZE`를 초과하면 `cacheable = 0`으로 플래그를 끄고, 누적을 중단한다. 전달은 계속한다 — 캐싱과 전달은 독립적이다.

## 테스트 하네스 설계

### 로컬 원본 서버 (`origin_server.py`)

Python `ThreadingHTTPServer`로 구현한 테스트용 원본 서버:
- `/cacheable/*`: 작은 텍스트 응답 (캐싱 가능)
- `/large/*`: 120KB 응답 (MAX_OBJECT_SIZE 초과 → 캐싱 불가)
- `/slow/*`: 2초 슬립 후 응답 (동시성 테스트)
- `/headers`: 수신한 헤더 에코 (헤더 재작성 검증)
- `/health`: 서버 준비 확인

### 테스트 흐름 (`run_proxy_tests.sh`)

1. 랜덤 포트로 원본 서버 시작
2. 랜덤 포트로 프록시 시작
3. `curl -x` (프록시 경유)로 각 테스트 케이스 실행
4. 동시성 테스트: 두 `/slow` 요청을 동시 발사, 총 소요 시간이 3.5초 미만인지 확인
5. 실패 복구: 존재하지 않는 서버에 요청 → 프록시가 살아남는지 확인
6. 캐시 테스트: 같은 URL 두 번 요청, 두 번째에서 `hit=1` (원본 서버는 `hit=2`를 반환하므로 캐시에서 서비스했음을 확인)

# Proxy Lab — 디버그 기록

## SIGPIPE로 프록시 전체가 사망

### 증상

클라이언트가 응답을 받는 도중 연결을 끊으면, 프록시 프로세스가 아무런 에러 메시지 없이 종료되었다.

### 원인

`rio_writen()`이 닫힌 소켓에 쓰면 커널이 `SIGPIPE`를 보낸다. `SIGPIPE`의 기본 동작은 프로세스 종료다. 한 클라이언트의 비정상 종료가 전체 프록시를 죽이는 것이다.

### 수정

```c
signal(SIGPIPE, SIG_IGN);
```

`main()`의 첫 줄에서 `SIGPIPE`를 무시한다. 이후 `rio_writen()`은 `EPIPE` 에러를 반환하고, 해당 연결만 정리하면 된다.

### 교훈

네트워크 서버에서 `SIGPIPE` 무시는 필수다. 클라이언트의 행동을 통제할 수 없으므로, 어떤 클라이언트가 연결을 끊어도 서버가 살아남아야 한다.

## 스레드에 clientfd를 스택 변수로 전달

### 증상

동시에 여러 요청을 보내면, 간헐적으로 잘못된 clientfd에 응답을 쓰는 문제가 발생했다. 한 클라이언트의 응답이 다른 클라이언트에게 전달되거나, `Bad file descriptor` 에러가 났다.

### 원인

```c
// 잘못된 코드
int clientfd = accept(listenfd, ...);
pthread_create(&tid, NULL, thread_main, &clientfd);  // 스택 변수의 주소!
```

메인 루프가 다음 `accept()`로 넘어가면 `clientfd`의 값이 새 연결의 fd로 바뀐다. 이미 생성된 스레드가 `&clientfd`를 역참조하면 새 fd를 보게 된다.

### 수정

```c
int *clientfd = malloc(sizeof(int));
*clientfd = accept(listenfd, ...);
pthread_create(&tid, NULL, thread_main, clientfd);
// 스레드에서 free(arg) 호출
```

힙 할당으로 각 스레드가 자신만의 fd 사본을 갖는다.

### 교훈

스레드에 인자를 전달할 때는 스레드의 수명과 변수의 수명이 일치하는지 확인해야 한다. 메인 루프의 스택 변수는 스레드가 읽기 전에 덮어씌워질 수 있다.

## 캐시 락을 쥐고 네트워크 I/O

### 증상

캐시를 추가한 뒤 동시성 테스트가 실패했다. 두 개의 `/slow` 요청이 3.5초 이상 걸렸다.

### 원인

초기 구현에서 `cache_lookup()`이 히트 시 락을 쥔 채 `rio_writen(clientfd, entry->data, entry->size)`를 호출했다. 캐시에 히트한 요청이 클라이언트에 응답을 쓰는 동안, 다른 모든 스레드가 캐시 락을 대기해야 했다.

### 수정

히트 시 데이터를 `malloc` + `memcpy`로 복사한 뒤 락을 해제하고, 복사본을 클라이언트에 전달한다:

```c
memcpy(copy, entry->data, entry->size);
pthread_mutex_unlock(&cache_lock);
rio_writen(clientfd, copy, size);
free(copy);
```

메모리 복사 비용이 추가되지만, 락 점유 시간이 극적으로 줄어든다.

### 교훈

"락 안에서 I/O를 하지 마라"는 동시성 프로그래밍의 기본 원칙이다. 락은 공유 상태를 보호하는 데만 사용하고, 최대한 빨리 놓아야 한다.

## URI에 포트가 없을 때 기본값 누락

### 증상

`http://example.com/path` (포트 없음) 형태의 URI에서 `open_clientfd(host, port)`가 실패했다. `port`가 빈 문자열이었다.

### 수정

`parse_uri()`에서 `memchr(host_start, ':', ...)`이 NULL을 반환하면 포트를 `"80"`으로 설정:

```c
if (colon != NULL) {
    // ... 포트 추출 ...
} else {
    strcpy(port, "80");
}
```

### 교훈

HTTP의 기본 포트(80)는 명시적으로 처리해야 한다. 브라우저는 포트를 생략하는 것이 일반적이다.

## 대형 객체의 캐시 무한 증가

### 증상

120KB 객체를 여러 번 요청하면, 프록시의 메모리 사용량이 계속 증가했다.

### 원인

`MAX_OBJECT_SIZE` 체크 없이 모든 응답을 캐시에 저장했다. 120KB 객체 10개면 1.2MB로 `MAX_CACHE_SIZE`(1MB)를 초과하지만, eviction 로직이 제대로 동작하지 않아 무한히 쌓였다.

### 수정

1. `cache_store()` 진입 시 `size > MAX_OBJECT_SIZE`이면 즉시 반환
2. 전달 중에 `object_size + n > MAX_OBJECT_SIZE`이면 `cacheable = 0` 플래그로 누적 중단

### 교훈

캐시 정책은 두 레벨에서 적용해야 한다: 개별 객체 크기 제한과 전체 캐시 크기 제한. 둘 다 빠지면 메모리 누수와 같은 증상이 나타난다.

# Proxy Lab — 지식 인덱스

## HTTP 프록시 기본

### 프록시 동작 흐름
```
클라이언트 → 프록시 → 원본 서버
         ←        ←
```
1. 클라이언트가 프록시에 연결
2. 프록시가 요청을 파싱하고 원본 서버에 전달
3. 원본 서버의 응답을 클라이언트에 전달
4. 양쪽 연결 닫기

### URI 파싱 (absolute-form)
```
http://host:port/path
```
- `host`: 원본 서버 주소
- `port`: 기본값 80
- `path`: 기본값 `/`

### 헤더 재작성 정책

| 헤더 | 동작 |
|---|---|
| `Host` | 프록시가 파싱한 host(:port) 설정 |
| `User-Agent` | 고정 CS:APP 값으로 대체 |
| `Connection` | `close` 강제 |
| `Proxy-Connection` | `close` 강제 |
| 기타 | 그대로 전달 |

### HTTP 버전 변환
- 클라이언트 → 프록시: HTTP/1.1 또는 HTTP/1.0
- 프록시 → 원본 서버: 항상 HTTP/1.0
- 이유: HTTP/1.0은 연결당 요청 하나, 구현이 단순

## 소켓 프로그래밍

### 서버 측
```c
int listenfd = open_listenfd(port);  // socket + bind + listen
int clientfd = accept(listenfd, ...);
```

### 클라이언트 측 (프록시 → 원본)
```c
int serverfd = open_clientfd(host, port);  // socket + connect
```

### Robust I/O (rio)
- `rio_readinitb()`: 버퍼 초기화
- `rio_readlineb()`: 개행 문자까지 한 줄 읽기
- `rio_readnb()`: 최대 n 바이트 읽기
- `rio_writen()`: 정확히 n 바이트 쓰기 (short write 처리)

## 동시성

### 스레드 모델 — per-connection threading

```c
while (1) {
    int *clientfd = malloc(sizeof(int));
    *clientfd = accept(listenfd, ...);
    pthread_create(&tid, NULL, thread_main, clientfd);
}
```

핵심 규칙:
- fd를 힙에 할당 (스택 변수 → 데이터 레이스)
- `pthread_detach(pthread_self())` — 조인 불필요, 자원 자동 회수
- `signal(SIGPIPE, SIG_IGN)` — 네트워크 서버 필수

### 뮤텍스 기본

```c
pthread_mutex_lock(&cache_lock);
// ... 공유 상태 접근 ...
pthread_mutex_unlock(&cache_lock);
```

원칙: 락 안에서 I/O를 하지 않는다. 공유 상태만 보호하고 빨리 놓는다.

## LRU 캐시

### 자료구조 — 이중 연결 리스트

```
cache_head ↔ [entry] ↔ [entry] ↔ ... ↔ [entry] ↔ cache_tail
(MRU)                                              (LRU)
```

### 연산

| 연산 | 설명 |
|---|---|
| lookup | 리스트 순회 → 히트: promote + 데이터 복사 반환 |
| store | LRU eviction → 헤드에 삽입 |
| promote | 엔트리를 리스트에서 빼서 헤드에 재삽입 |
| evict | 테일에서 빼기 + free |

### 크기 제한

| 상수 | 값 | 의미 |
|---|---|---|
| `MAX_CACHE_SIZE` | 1,048,576 (1MB) | 전체 캐시 최대 크기 |
| `MAX_OBJECT_SIZE` | 102,400 (100KB) | 단일 객체 최대 크기 |

### 캐싱 판정 흐름
1. 응답 수신 중: `object_buf`에 누적, 크기가 `MAX_OBJECT_SIZE` 초과 시 `cacheable = 0`
2. 수신 완료 후: `cacheable && object_size > 0`이면 `cache_store()` 호출
3. `cache_store()`: 총 크기 초과 시 LRU부터 evict

## 에러 처리

| 상황 | 응답 |
|---|---|
| 잘못된 요청 라인 | 400 Bad Request |
| GET 외 메서드 | 501 Not Implemented |
| 원본 서버 연결 실패 | 502 Bad Gateway |
| 요청 너무 큼 | 400 Bad Request |
| SIGPIPE | SIG_IGN (프록시 생존) |

## 테스트 인프라

### 원본 서버 (origin_server.py)

| 엔드포인트 | 동작 |
|---|---|
| `/health` | 서버 준비 확인 |
| `/cacheable/*` | 작은 텍스트 + 히트 카운터 |
| `/large/*` | 120KB 응답 (MAX_OBJECT_SIZE 초과) |
| `/slow/*` | 2초 딜레이 (동시성 테스트) |
| `/headers` | 수신 헤더 에코 |

### 테스트 케이스 요약

| 테스트 | 검증 내용 |
|---|---|
| 기본 전달 | GET 요청/응답 프록싱 |
| 헤더 재작성 | Host, User-Agent, Connection 강제 대체 |
| 캐시 히트 | 같은 URL 두 번 → 두 번째에서 hit=1 잔존 |
| 대형 객체 | 120KB → 캐싱 안 됨 → 두 번째에서 hit=2 |
| 동시성 | 두 slow 요청 동시 → 총 시간 < 3.5초 |
| 실패 복구 | 죽은 서버 요청 후 정상 서비스 지속 |

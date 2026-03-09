# Proxy Lab — 개발 타임라인

이 문서는 소스 코드에 드러나지 않는 개발 과정의 시간 순서, 사용한 CLI 명령, 환경 구축 절차를 기록한다.

---

## Phase 1: 문제 환경 준비

### CS:APP 헬퍼 배치

`problem/code/`에 `csapp.c`, `csapp.h` 배치. 프록시 구현이 의존하는 소켓 래퍼(`open_clientfd`, `open_listenfd`)와 Robust I/O(`rio_*`) 함수를 포함한다.

### starter proxy 배치

`problem/code/proxy.c` — 기본 스켈레톤.

### 빌드 확인

```bash
cd study/Systems-Programming/proxylab/problem
make clean && make
```

---

## Phase 2: C 트랙 — 마일스톤 1 (순차 전달)

### 구현

`c/src/proxy.c`에서:
1. `parse_uri()` — absolute-form URI 파싱 (host, port, path 추출)
2. `build_request()` — HTTP/1.0 요청 재구성 + 헤더 정책 적용
3. `handle_client()` — 요청 파싱 → 원본 연결 → 전달 → 응답 파이프

### 수동 테스트

```bash
cd c && make
./build/proxy 8080 &
curl -x http://127.0.0.1:8080 http://example.com/
```

---

## Phase 3: C 트랙 — 마일스톤 2 (동시 처리)

### 구현

```c
// main() accept 루프
int *clientfd = malloc(sizeof(int));
*clientfd = accept(listenfd, ...);
pthread_create(&tid, NULL, thread_main, clientfd);

// thread_main()
pthread_detach(pthread_self());
free(arg);
handle_client(clientfd);
close(clientfd);
```

`signal(SIGPIPE, SIG_IGN)` 추가.

### 빌드

```bash
cd c
make clean && make
# -lpthread 링크 플래그 필요
```

---

## Phase 4: C 트랙 — 마일스톤 3 (캐시)

### 구현

이중 연결 리스트 + `pthread_mutex_t`:
- `cache_entry_t` 구조체 (uri, data, size, prev, next)
- `cache_lookup()` — 순회, promote, 데이터 복사 후 락 해제
- `cache_store()` — eviction + 헤드 삽입

### 핵심 정책
- `MAX_CACHE_SIZE = 1048576` (1MB)
- `MAX_OBJECT_SIZE = 102400` (100KB)

---

## Phase 5: 테스트 하네스 구축

### 원본 서버

`tests/origin_server.py` 작성 — Python `ThreadingHTTPServer`:
- `/cacheable/*`, `/large/*`, `/slow/*`, `/headers`, `/health` 엔드포인트

### 테스트 스크립트

`tests/run_proxy_tests.sh` 작성 — 6개 테스트 케이스:
1. 기본 전달
2. 헤더 재작성 (Host, User-Agent, Connection, Proxy-Connection, X-Test 전달)
3. 캐시 히트 (같은 URL 두 번)
4. 대형 객체 캐싱 안 됨 (120KB > MAX_OBJECT_SIZE)
5. 동시성 (두 slow 요청 병렬, 총 시간 < 3.5초)
6. 실패 복구 (죽은 서버 → 정상 서비스 지속)

### 검증

```bash
cd c
make clean && make test
```

---

## Phase 6: C++ 트랙

### 구현

C 트랙과 동일한 로직을 C++ 스타일로 재구현.

### 검증

```bash
cd study/Systems-Programming/proxylab/cpp
make clean && make test
```

---

## Phase 7: 문서 작성

### docs/ 구성

- `docs/concepts/http-forwarding.md` — URI 파싱, 헤더 정책, 에러 처리
- `docs/concepts/concurrency-and-cache.md` — 스레드 모델, LRU 캐시 설계, 락 규칙
- `docs/references/verification.md` — 검증 명령, 테스트 커버리지, 현재 결과

---

## 의존성 요약

| 항목 | 내용 |
|---|---|
| 컴파일러 | gcc (C99 + `_POSIX_C_SOURCE=200809L`) |
| 빌드 | make, `-lpthread` |
| CS:APP 헬퍼 | `problem/code/csapp.c`, `csapp.h` |
| 테스트 도구 | Python 3 (`ThreadingHTTPServer`), curl, bash |
| 외부 의존성 | 없음 (Docker 불필요) |
| 로컬 환경 | macOS (POSIX 호환) |

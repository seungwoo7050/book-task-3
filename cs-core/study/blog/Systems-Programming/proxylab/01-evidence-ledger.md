# Proxy Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`proxylab`은 HTTP 요청 파싱, header 정규화, concurrent connection 처리, in-memory cache 설계를 하나의 프록시 구현으로 묶는 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/proxy.c`, `cpp/src/proxy.cpp`다. 검증 표면은 `tests/origin_server.py`, `tests/run_proxy_tests.sh`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `concurrency and cache`, `http forwarding`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - URI 파싱과 upstream request 조립을 먼저 세운다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 프록시의 첫 번째 일은 캐시가 아니라 올바른 요청을 origin으로 다시 보내는 일이다.

그때 세운 가설은 header 정규화 전에 `parse_uri`와 `build_request`가 흔들리면 네트워크 디버깅이 전부 흐려질 거라고 봤다. 실제 조치는 URI 파싱, header append helper, canonical request builder를 먼저 묶어 upstream surface를 고정했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/proxy.c`
- CLI: `make clean && make test`
- 검증 신호: request builder가 먼저 고정돼 있어 이후 캐시/동시성 문제를 분리해서 볼 수 있다.
- 새로 배운 것: 네트워크 프로그램도 초기 단계는 소켓보다 문자열 계약을 얼마나 안정적으로 다루는지가 더 중요했다.

### 코드 앵커 — `parse_uri` (`c/src/proxy.c:156`)

```c
static int parse_uri(const char *uri, char *host, char *port, char *path)
{
    const char *host_start = uri;
    const char *path_start;
    const char *colon;
    size_t host_len;
```

이 조각은 request builder가 먼저 고정돼 있어 이후 캐시/동시성 문제를 분리해서 볼 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Parse_Uri`를 읽고 나면 다음 장면이 왜 concurrent serve와 cache path로 넘어간다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `Build_Request` (`c/src/proxy.c:37`)

```c
static int build_request(char *request, size_t capacity, const char *host, const char *port,
                         const char *path, rio_t *client_rio);
static int cache_lookup(const char *uri, char **data_out, size_t *size_out);
static void cache_store(const char *uri, const char *data, size_t size);
```

이 조각은 request builder가 먼저 고정돼 있어 이후 캐시/동시성 문제를 분리해서 볼 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Build_Request`를 읽고 나면 다음 장면이 왜 concurrent serve와 cache path로 넘어간다로 이어지는지도 한 번에 보인다.

다음 단계에서는 concurrent serve와 cache path로 넘어간다.

## 2. Phase 2 - 동시성 처리와 LRU cache를 serve path에 붙인다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `handle_client`, `cache_lookup`, `cache_store`, `promote_entry`가 실제 프록시의 중간 설계 축이다.

그때 세운 가설은 멀티클라이언트 처리를 붙이는 순간 캐시 일관성과 request forwarding이 함께 흔들릴 거라고 예상했다. 실제 조치는 client handler에서 forwarding과 caching을 한 번에 다루되, cache list 조작은 helper로 분리해 LRU 이동을 명확히 했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/proxy.c`
- CLI: `make clean && make test`
- 검증 신호: cache helper 분리가 있어야 동시성과 캐시 논의를 같은 파일 안에서도 추적할 수 있다.
- 새로 배운 것: 캐시는 성능 기능이 아니라 concurrent serve path를 깨뜨리지 않으면서 반복 요청을 흡수하는 별도 contract였다.

### 코드 앵커 — `handle_client` (`c/src/proxy.c:245`)

```c
static void handle_client(int clientfd)
{
    char buf[MAXLINE];
    char method[MAXLINE];
    char uri[MAXLINE];
    char version[MAXLINE];
    char host[MAXLINE];
    char port[MAXLINE];
    char path[MAXLINE];
    char request[MAX_REQUEST_SIZE];
    char *cached_data = NULL;
    size_t cached_size = 0;
```

이 조각은 cache helper 분리가 있어야 동시성과 캐시 논의를 같은 파일 안에서도 추적할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Handle_Client`를 읽고 나면 다음 장면이 왜 self-owned origin server로 전체 루프를 검증한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `cache_lookup` (`c/src/proxy.c:78`)

```c
static int cache_lookup(const char *uri, char **data_out, size_t *size_out)
{
    cache_entry_t *entry;
    char *copy;
```

이 조각은 cache helper 분리가 있어야 동시성과 캐시 논의를 같은 파일 안에서도 추적할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Cache_Lookup`를 읽고 나면 다음 장면이 왜 self-owned origin server로 전체 루프를 검증한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 self-owned origin server로 전체 루프를 검증한다.

## 3. Phase 3 - origin server 기반 end-to-end test로 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 proxy는 unit-level helper만으로 끝나지 않고 실제 요청/응답 루프를 확인해야 한다.

그때 세운 가설은 공식 driver 없이도 `tests/origin_server.py`와 shell harness가 있으면 구현 흐름을 충분히 재현할 수 있다고 판단했다. 실제 조치는 README와 Makefile을 `run_proxy_tests.sh` 중심으로 묶어 end-to-end 검증을 공개 표면에 올렸다.

- 정리해 둔 근거:
- 변경 단위: `tests/run_proxy_tests.sh`, `tests/origin_server.py`
- CLI: `make clean && make test`
- 검증 신호: origin fixture와 shell harness가 마지막 검증 신호를 남긴다.
- 새로 배운 것: 네트워크 프로그램일수록 self-owned origin fixture가 reasoning을 재현하는 핵심 자산이 됐다.

### 코드 앵커 — `Handler` (`tests/origin_server.py:14`)

```python
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, format, *args):
        return
```

이 조각은 origin fixture와 shell harness가 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `Handler`를 읽고 나면 다음 장면이 왜 request surface, concurrent handler, cache verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `$ORIGIN_PID` (`tests/run_proxy_tests.sh:26`)

```bash
    if [[ -n "$ORIGIN_PID" ]]; then
        kill "$ORIGIN_PID" 2>/dev/null || true
        wait "$ORIGIN_PID" 2>/dev/null || true
    fi
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT
```

이 조각은 origin fixture와 shell harness가 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `$ORIGIN_PID`를 읽고 나면 다음 장면이 왜 request surface, concurrent handler, cache verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 request surface, concurrent handler, cache verification 순서로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c && make clean && make test)
```

```text
Proxy tests passed
bash ../tests/run_proxy_tests.sh ./build/proxy
```
